$(document).ready(function() {
    const genreSearchInput = $("#genre-search");
    const genreResultsDiv = $("#genre-search-results");
    const topSongsByGenreTable = $("#top-songs-by-genre tbody");
    const topSongsByGenreTitle = $("#top-songs-by-genre-title");

    genreSearchInput.on("keyup", function() {
        const query = $(this).val();
        if (query.length > 0) {
            fetchGenres(query);
            genreResultsDiv.show();
        } else {
            genreResultsDiv.empty().hide();
        }
    });

    genreResultsDiv.on('click', 'p', function() {
        const selectedGenre = $(this).text();
        fetchTopSongsByGenre(selectedGenre);
        topSongsByGenreTitle.text(`Top Songs in ${selectedGenre}`);
        genreSearchInput.val(selectedGenre);
        genreResultsDiv.empty().hide();
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

    function fetchTopSongsByGenre(genre) {
        $.get("/top-songs-by-genre", { genre: genre }, function(songs) {
            topSongsByGenreTable.empty();
            genreResultsDiv.hide(); // Hide the genre list
    
            if (songs && songs.length > 0) {
                songs.forEach(song => {
                    let creatorsHtml = song.creators.map(creator =>
                        `<a href="/profile/${creator.id}">${creator.username}</a>`
                    ).join(', ');
                    topSongsByGenreTable.append(`
                        <tr>
                            <td>${song.name}</td>
                            <td>${creatorsHtml}</td>
                            <td>${song.popularity}</td>
                        </tr>
                    `);
                });
            } else {
                topSongsByGenreTable.append("<tr><td colspan='3'>No songs found in this genre.</td></tr>");
            }
        });
    }
});
