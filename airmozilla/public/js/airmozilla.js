(function() {
  function escapeHTML(str) {
      var div = document.createElement('div');
      div.appendChild(document.createTextNode(str));
      return div.innerHTML;
  }

  var button = document.getElementById('load-more-events');
  var container = document.getElementById('recent-container');

  button.addEventListener('click', function(event) {
    var offset = container.querySelectorAll('.event').length;

    button.classList.add('loading');

    fetch(DJANGO_META.URLS['load-more'] + '?offset=' + offset)
      .then(function(response) {
        return response.text();
      }).then(function(body) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(body, 'text/html');

        if (doc.querySelectorAll('.event').length < DJANGO_META.PAGE_SIZE) {
          button.remove();
        }

        doc.querySelectorAll('.event').forEach(function(event) {
          container.appendChild(event);
        });

        button.classList.remove('loading');
      });

    event.preventDefault();
  });

  autocomplete('#search-input', {openOnFocus: true, autoselect: true, minLength: 3}, [
    {
      source: function(query, cb) {
        fetch(DJANGO_META.URLS.search + '?q=' + encodeURIComponent(query))
          .then(function(response) {
            return response.json();
          }).then(function (json) {
            cb(json.results);
          });
      },
      templates: {
        suggestion: function(suggestion) {
          return (
            '<p><a target="_blank" href="' +
            escapeHTML(suggestion.link) +
            '">' +
            escapeHTML(suggestion.title) +
            '</a></p>'
          );
        },
        empty: function(context) {
          return '<p class="empty">No results for "' + escapeHTML(context.query) + '".</p>';
        }
      }
    }
  ]).on('autocomplete:selected', function(event, suggestion, dataset) {
    window.open(suggestion.link);
  });
})()
