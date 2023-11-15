$(document).ready(function() {
    const genreSearchInput = $("#genre-search");
    const genreResultsDiv = $("#genre-search-results");

    genreSearchInput.on("keyup", function() {
        const query = $(this).val();
        fetchGenres(query);
    });

    function fetchGenres(query) {
        $.get("/search-genre", { genre_name: query }, function(genres) {
            genreResultsDiv.empty();

            if (genres && genres.length > 0) {
                // Display top 10 results as clickable items
                genres.slice(0, 10).forEach(genre => {
                    genreResultsDiv.append(`<p>${genre.Name}</p>`);
                });
            } else {
                genreResultsDiv.append("<p>No genres found</p>");
            }
        });
    }
});
