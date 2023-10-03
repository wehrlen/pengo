document.addEventListener('DOMContentLoaded', function() {
    console.log("test")
    var test;
    
    $(document).ready(function(){
      $.getJSON('all_events/', 
      function(data) {
          test = data
          console.log(test)
          data_test()
      })
    
    
      function data_test(){
        console.log(test)
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          timeZone: 'Europe/Paris',
          locale: 'fr',
          initialView: 'dayGridMonth',
          headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,listWeek,timeGridDay' // user can switch between the two
          },
          events: "all_events/",
          eventColor: '#378006',
          selectable: true,
          editable: true,
          select: function (start, end, allDay) {
            var title = prompt("Enter Event Title");
            if (title) {
              
              console.log(start.endStr)
              var end= start.endStr;
              var start = start.startStr;

              
              $.ajax({
                type: "GET",
                url: 'add_event',
                data: {'title': title, 'start': start, 'end': end},
                dataType: "json",
                success: function (data) {
                  calendar.refetchEvents()
                  alert('Event Update');
                },
                error: function (data) {
                  alert('There is a problem!!!');
                }
              });
            }
          },
        });
        calendar.render();

        //var event = calendar.getJSON // an event object!
        //console.log(event)

      }
    });
  

});
/*$(document).ready(function(){
    $.getJSON('all_events/', 
    function(data) {
        console.log(data)
})
});*/
