document.addEventListener("DOMContentLoaded", () => {
  const calendarEl = document.querySelector("#calendar");
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "listWeek",
    views: {
      listDay: { buttonText: 'list day' },
      listWeek: { buttonText: 'list week' },
      listMonth: { buttonText: 'list month' }
    },
    headerToolbar: {
      left: 'title',
      center: 'today prev,next',
      right: 'listDay,listWeek,listMonth'
    },
    eventClick: function(info) {
      info.el.style.backgroundColor = info.el.style.backgroundColor === "white" ? "rgb(100 200 100)" : "white";
    },
    eventContent: function(arg) {
      return {html: arg.event._def.title};
    }
  });
  calendar.render();

  const form = document.querySelector("#bot-form")
  form.addEventListener("submit", async (e) => {
    e.preventDefault()
    formData = new FormData(form)
    const content = await fetch("http://localhost:5000/calendar/bot", {
      method: "POST",
      body: formData
    })

    const ev = await content.json()
    calendar.addEvent(ev)
  })
})
