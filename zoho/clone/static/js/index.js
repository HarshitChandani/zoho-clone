var log_hours = new Object();
var attendence_timer;
var sum_ttl_work_hr = [0,0];
var log_hour_obj = {}

// Function will add new rows in the table when add row button get clicked
add_job_row = () => {
   var table_obj = document.getElementById("time-tracker-table");
   var cnt_rows = table_obj.rows.length;
   var new_row = table_obj.rows[1].cloneNode(true);

   var sr_no_box = `<input type='text' value=${cnt_rows} class='form-control daily-log-field' readonly>`
   var job_title_box = `<input type='text' name='job-title-${cnt_rows}' class='form-control w-100 daily-log-field' id='job-title-${cnt_rows}'>` 
   var job_description_box = `<input type='text' name='job-description-${cnt_rows}' class='form-control w-100 daily-log-field' id='job-description-${cnt_rows}'>` 
   var job_hour_box = `<input type='text' name='job-hour-${cnt_rows}'class='form-control w-100 daily-log-field' maxlength='5' id='job-hour-${cnt_rows}' onkeyup='daily_log_hours(this)'>`

   new_row.cells[0].innerHTML = sr_no_box;
   new_row.cells[1].innerHTML = job_title_box;
   new_row.cells[2].innerHTML = job_description_box;
   new_row.cells[3].innerHTML = job_hour_box

   table_obj.appendChild(new_row);
}

get_current_date = () => {
   let attendence_date = new Date();
   var dd = String(attendence_date.getDate()).padStart(2, '0');
   var mm = String(attendence_date.getMonth() + 1).padStart(2, '0'); //January is 0!
   var yyyy = attendence_date.getFullYear();
   attendence_date = `${yyyy}-${mm}-${dd}`
   return attendence_date
}

// Funtion will return current time in seconds timestamp.
get_current_time = () =>{
   let curr_time = new Date().getTime()
   return curr_time
}

// IMP: Logic of below function
add_log_work_hours = (a_time,b_time) => {
   var a = a_time.split(':')
   var b = b_time.split(':')

   for (var i=0; i<2; i++){
      a[i] = isNaN(parseInt(a[i])) ? 0 : parseInt(a[i])
      b[i] = isNaN(parseInt(b[i])) ? 0 : parseInt(b[i])
      sum_ttl_work_hr[i] = a[i] + b[i]
   }

   var hours = sum_ttl_work_hr[0]
   var minutes = sum_ttl_work_hr[1]
   
   if ( minutes > 60){
      var remaining = ( minutes / 60 ) | 0         // bitwise OR operator 
      hours += remaining
      minutes = minutes - (60 * remaining)
      minutes = minutes < 10 ? `0${minutes}` : minutes 
      hours = hours < 10 ? `0${hours}` : hours
   }
   result = `${hours}:${minutes}`
   return result
}

// Function will count the total work job hours of the timesheet 
daily_log_hours = (element) => {
   ttl_work_hrs = document.getElementById('ttl-work-hours').value
   log_hour = document.getElementById(element.id).value
   if (log_hour.includes(":")){
      log_hour_obj[element.id] = log_hour
      if (ttl_work_hrs != null && ! log_hour_obj.hasOwnProperty('ttl-work-hours')){
         log_hour_obj['ttl-work-hours'] = ttl_work_hrs
      }
   }
   document.getElementById('ttl-work-hours').value = Object.values(log_hour_obj).reduce(add_log_work_hours)
}

// Function will save the time sheet data to the storage.
save_timetracker_data = () => {
   var job = new Object();
   const csrf_token = $("input[name=csrfmiddlewaretoken]").val();
   
   var table_obj = document.getElementById("time-tracker-table");
   var cnt_rows = table_obj.rows.length;
   
   var date = new Date();
   job.date =  `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`
   for (var i=0; i< (cnt_rows-1); i++){
     job[`job${i+1}`] ={
         'title': document.getElementById(`job-title-${i+1}`).value,
         'description':document.getElementById(`job-description-${i+1}`).value,
         'hour':document.getElementById(`job-hour-${i+1}`).value
      } 
   }
   print(job)
   ttl_work_hr = document.getElementById('ttl-work-hours').value
   job_json = JSON.stringify(job)
   $.ajax({
      method:"POST",
      url: "/time-tracker/",
      data: {
         job_data: job_json,
         ttl_work_hr: ttl_work_hr
      },
      headers:{
         'X-CSRFToken':csrf_token
      },
      success: (data)=>{
         if (data.recorded) {
            alert('Data has been saved.')
            window.location.href = '/time-tracker/'
         }
      }
   });
}

// Execute when use click the check-in button
check_in = () => {
   const csrf_token = $("input[name=csrfmiddlewaretoken]").val();
      
   const check_in_time = get_current_time();
   localStorage.setItem('checkin_time',check_in_time)
   localStorage.setItem('checkin_date',get_current_date())
   
   $.ajax({
      method:'POST',
      url : '/attendence/',
      data : {
         action:'in',
         checkin:check_in_time,
         date:localStorage.getItem('checkin_date') 
      },
      headers:{
         'X-CSRFToken':csrf_token
      },
      success: (response) => {
         if (response.checked_in){
            get_time_difference()
            document.getElementById("check-in-btn").style.display = "none"
            document.getElementById("check-out-btn").style.display = "block"
            localStorage.setItem('record-id',response.record_id)
            localStorage.setItem('attendence-id',response.attendence_id)
            localStorage.setItem('checked-in-status',true)
         }
         else{
            alert('Error occured . Please try after some time.')
         }
      } 
   })
   
}

// Function to calculate the difference between check-in time and current time.
get_time_difference = () => {
   if (localStorage.getItem('checkin_time') != null){
      const checkin_time = localStorage.getItem('checkin_time')
      
      attendence_timer = setInterval( function(){
         
         let current_time = get_current_time()
         let diff = current_time - checkin_time
         let hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
         let min = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
         let sec = Math.floor((diff % (1000 * 60)) / 1000);
         min = min < 10 ? `0${min}` : min
         hours = hours < 10 ? `0${hours}` : hours
         sec = sec < 10 ? `0${sec}` : sec
         var time = `${hours}:${min}:${sec}`

         document.getElementById("hidden_attendence_timer").value=time
         document.getElementById("timer").innerHTML = time; 
   
      },1000);
      document.getElementById("check-in-btn").style.display = "none";
      document.getElementById("check-out-btn").style.display = "block"; 
   }
   else{
      document.getElementById("check-in-btn").style.display = "block";
      document.getElementById("check-out-btn").style.display = "none";    
   }
}

// Executes when user click check-out time.
check_out = () =>{

   // new Date().getTime() is in milliseconds so divide it by 1000 to get the second representation
   const record_attendence_time = document.getElementById("hidden_attendence_timer").value;
   clearInterval(attendence_timer)
   
   const csrf_token = $("input[name=csrfmiddlewaretoken]").val();
   
   const check_out_time = get_current_time()
   $.ajax({
      method:"POST",
      url:'/attendence/',
      headers:{
         'X-CSRFToken':csrf_token
      },
      data:{
         checkout: check_out_time,
         action: 'out',
         record_id: localStorage.getItem('record-id'),
         attendence_id: localStorage.getItem('attendence-id'),
         ttl_work_hrs : record_attendence_time,
      },
      success: (data) => {
         console.info(data)
         if (data.success){
            localStorage.removeItem('checkin_time')
            localStorage.removeItem('checkin_date')
            localStorage.removeItem('record-id')
            localStorage.removeItem('attendence-id')  
            get_time_difference()
         }
         else{
            alert("Error Occured. Please try after some time.")
         }
      }
   })
}

get_attendence_by_date = (attendence_id="") => {
   if (attendence_id != "" ){
      $.ajax({
         method:"GET",
         url:"/attendence-by-date/",
         data:{
            'attendence_id':attendence_id
         },
         success: (response) => {
            json_data = JSON.parse(response)
            $("#attendence-data-table-body").children().remove()
            var attendence_table_obj = document.getElementById('attendence-data-table-body')
            for(const data in json_data){
               cell = document.createElement("tr")
               check_in_time = moment(json_data[data].fields["check_in"],"hh:mm:ss A")
               check_out_time = moment(json_data[data].fields["check_out"],"hh:mm:ss A")
               total_hrs_time = moment(json_data[data].fields["total_hours"],"hh:mm:ss")

               check_in_block = document.createElement("td")
               check_out_block = document.createElement("td")
               total_hr_block = document.createElement("td")
               check_in_block.innerHTML = `${check_in_time.hours()}:${check_in_time.minutes()}:${check_in_time.seconds()}`
               check_out_block.innerHTML = `${check_out_time.hours()}:${check_out_time.minutes()}:${check_out_time.seconds()}`
               total_hr_block.innerHTML = `${total_hrs_time.hours()}:${total_hrs_time.minutes()}:${total_hrs_time.seconds()}`
               
               cell.appendChild(check_in_block)
               cell.appendChild(check_out_block)
               cell.appendChild(total_hr_block)
               attendence_table_obj.appendChild(cell)
            }
            $("#attendenceDataModal").modal('show')
         }
      })
     
      }
   else{
      alert("No Data Found")
   }
   
}

// Pending Bug: When User check-in for the multiple times in a day . Timer restarts from the 00:00:00 .
// When day changes the timer auto reset to 00:00:00

