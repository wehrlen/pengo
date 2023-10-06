document.addEventListener('DOMContentLoaded', function () {
  var test;

  $(document).ready(function () {
    $.getJSON('all_events/',
      function (data) {
        test = data
        data_test()
      })


    function data_test() {
      var calendarEl = document.getElementById('calendar');
      var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'fr',
        initialView: 'dayGridMonth',
        themeSystem: 'default',
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
            var end = start.endStr;
            var start = start.startStr;

            $.ajax({
              type: "GET",
              url: 'add_event',
              data: { 'title': title, 'start': start, 'end': end },
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

        eventResize: function (info) {
          var start = calendar.formatDate(info.event.start, {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          });
          var end = calendar.formatDate(info.event.end, {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          });

          var id = info.event.id
          $.ajax({
            type: "GET",
            url: 'update',
            data: { 'start': start, 'end': end, 'id': id },
            dataType: "json",
            success: function (data) {
              calendar.refetchEvents()
              alert('Event Update');
            },
            error: function (data) {
              alert('There is a problem!!!');
            }
          });
        },

        eventDrop: function (info) {

          var start = calendar.formatDate(info.event.start, {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          });
          var end = calendar.formatDate(info.event.end, {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          });

          var id = info.event.id
          $.ajax({
            type: "GET",
            url: 'update',
            data: { 'start': start, 'end': end, 'id': id },
            dataType: "json",
            success: function (data) {
              calendar.refetchEvents();
              alert('Event Update');
            },
            error: function (data) {
              alert('There is a problem!!!');
            }
          });


        },

        eventClick: function (info) {
          var event = info.event
          clickedEventId = event.id
          clickedEventStart = event.start
          clickedEventEnd = event.end
          document.getElementById('eventTitle').value = event.title;
          //document.getElementById('eventStart').value= event.start.toLocaleString();
          //document.getElementById('eventEnd').value = event.end.toLocaleString();

          var eventModal = document.getElementById('eventModal');
          eventModal.style.display = "block";
        }
      });
      calendar.render();
      var updateEventBtn = document.getElementById('updateEventBtn');
      updateEventBtn.addEventListener('click', function () {

        var newTitle = document.getElementById('eventTitle').value;
        var newStart = document.getElementById('eventStart').value;
        var newEnd = document.getElementById('eventEnd').value;

        if (!newStart) {
          newStart = clickedEventStart.toLocaleString()
        }

        if (!newEnd) {
          newEnd = clickedEventEnd.toLocaleString()
        }


        $.ajax({
          type: "GET",
          url: 'update',
          data: { 'title': newTitle, 'start': newStart, 'end': newEnd, 'id': clickedEventId },
          dataType: "json",
          success: function (data) {
            calendar.refetchEvents();
            alert('Event Update');
          },
          error: function (data) {
            alert('There is a problem!!!');
          }
        });

        // Fermez la modal en mode édition
        eventModal.style.display = "none";
      });

      // Gestionnaire d'événement pour le bouton de suppression
      var deleteEventBtn = document.getElementById('deleteEventBtn');
      deleteEventBtn.addEventListener('click', function () {

        $.ajax({
          type: "GET",
          url: 'remove',
          data: { 'id': clickedEventId },
          dataType: "json",
          success: function (data) {
            eventModal.style.display = "none";
            calendar.refetchEvents();
            alert('Event Removed');
            

          },
          error: function (data) {
            alert('There is a problem!!!');
          }
        });
      });
      var closeModalBtn = document.getElementById('closeModalBtn');
      closeModalBtn.addEventListener('click', function () {
        eventModal.style.display = "none";
      });

    }
  });
});

