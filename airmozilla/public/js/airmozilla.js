(function() {
  var button = document.getElementById('load-more-events');
  var container = document.getElementById('recent-container');

  button.addEventListener('click', function(event) {
    var offset = container.querySelectorAll('.event').length;

    button.classList.add('loading');

    fetch('/load-more/?offset=' + offset)
      .then(function(response) {
        return response.text();
      }).then(function(body) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(body, 'text/html');

        if (doc.querySelectorAll('.event').length < 16) {
          button.remove();
        }

        doc.querySelectorAll('.event').forEach(function(event) {
          container.appendChild(event);
        });

        button.classList.remove('loading');
      });

    event.preventDefault();
  });
})()
