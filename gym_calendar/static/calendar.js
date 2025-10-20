document.addEventListener("DOMContentLoaded", async () => {
  const res = window.location.href.includes("localhost") ? await fetch("http://localhost:5000/calendar/history") : await fetch(`${window.location.origin}/calendar/history/`, {method: "GET", credentials: "same-origin"});
  const oldEvents = await res.json() || [];
  const calendarEl = document.querySelector("#calendar");
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "listWeek",
    events: oldEvents,
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
    const url = window.location.href.includes("localhost") ? "http://localhost:5000/calendar/bot" : `${window.location.origin}/calendar/bot/`
    const content = await fetch(url, {
      method: "POST",
      body: formData,
      credentials: "same-origin"
    })

    const evs = await content.json();
    evs.map(work => {
      calendar.addEvent(work);
    })
  })
})
