$(document).ready(function() {
    const searchInput = $("#song-search");
    const resultsDiv = $("#search-results tbody");
    const searchButton = $("#search-button");

    searchInput.on("keyup", function(e) {
        const query = $(this).val();
        const isEnterPressed = e.which === 13;

        // If Enter is pressed, search and increment popularity
        if (isEnterPressed) {
            performSearch(query, true);
        } else if (query.length > 2) {
            // If the user is typing, just get top 10 results without incrementing popularity
            performSearch(query, false);
        } else {
            resultsDiv.empty();
        }
    });

    searchButton.on("click", function() {
        const query = searchInput.val();
        performSearch(query, true);
    });

    resultsDiv.on('click', 'p', function() {
        const chosenSong = $(this).text();
        searchInput.val(chosenSong);
        performSearch(chosenSong, true);
    });

    function performSearch(query, incrementPopularity) {
        $.get("/search", { song_name: query, increment_popularity: incrementPopularity }, function(data) {
            displaySearchResults(data, incrementPopularity);
        });
    }

    function displaySearchResults(data, incrementPopularity) {
        if (data && data.length > 0) {
            if (incrementPopularity) {
                resultsDiv.empty();
                data.forEach(song => {
                    resultsDiv.append(`
                        <tr>
                            <td>${song.name}</td>
                            <td>${song.upload_date}</td>
                            <td>${song.upload_user}</td>
                            <td>${song.popularity}</td>
                            <td>${song.filepath}</td>
                        </tr>
                    `);
                });
            } else {
                $('#search-suggestions').empty();
                data.forEach(function(song) {
                    $('<option>').val(song.name).appendTo('#search-suggestions');
                });
            }
        } else {
            resultsDiv.empty();
            resultsDiv.append("<p>No results found</p>");
        }
    }
});
