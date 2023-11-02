$(document).ready(function() {
    const searchInput = $("#song-search");
    const resultsDiv = $("#search-results tbody");

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

    resultsDiv.on('click', 'p', function() {
        const chosenSong = $(this).text();
        searchInput.val(chosenSong);
        performSearch(chosenSong, true);
    });

    function performSearch(query, incrementPopularity) {
        $.get("/search", { song_name: query, increment_popularity: incrementPopularity }, function(data) {
            resultsDiv.empty();

            if (data && data.length > 0) {
                if (incrementPopularity) {
                    // Display results in table format
                    data.forEach(song => {
                        resultsDiv.append(`
                            <tr>
                                <td>${song.name}</td>
                                <td>${song.upload_date}</td>
                                <td>${song.popularity}</td>
                                <td>${song.filepath}</td>
                            </tr>
                        `);
                    });
                } else {
                    // Display top 10 results as clickable items 
                    data.forEach(song => {
                        resultsDiv.append(`<p>${song.name}</p>`);
                    });
                }
            } else {
                resultsDiv.append("<p>No results found</p>");
            }
        });
    }
});
