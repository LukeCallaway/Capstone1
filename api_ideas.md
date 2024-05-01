WatchMode \
https://api.watchmode.com/docs/

### example of serching by title breaking bad
useful for having basic info for searching and making sure you have the correct movie title \
can set parameters to only search for movies \
{ 

  "results": [

    {

      "name": "Breaking Bad",

      "relevance": 445.23,

      "type": "tv_series",

      "id": 3173903,

      "year": 2008,

      "result_type": "title",

      "tmdb_id": 1396,

      "tmdb_type": "tv",

      "image_url": "https://cdn.watchmode.com/posters/03173903_poster_w185.jpg"

    },

    {

      "name": "El Camino: A Breaking Bad Movie",

      "relevance": 169.83,

      "type": "movie",

      "id": 1586594,

      "year": 2019,

      "result_type": "title",

      "tmdb_id": 559969,

      "tmdb_type": "movie",

      "image_url": "https://cdn.watchmode.com/posters/01586594_poster_w185.jpg"

    }

  ]
  
}

### example of searching for a specific movie
information available: title, release year, rated, runtime, genre, trailer, where to watch, plot, movie poster, ratings, similar titles

{

  "id": 3173903,

  "title": "Breaking Bad",

  "original_title": "Breaking Bad",

  "plot_overview": "When Walter White, a New Mexico chemistry teacher, is diagnosed with Stage III 
  cancer and given a prognosis of only two years left to live. He becomes filled with a sense of fearlessness and an unrelenting desire to secure his family's financial future at any cost as he enters the dangerous world of drugs and crime.",

  "type": "tv_series",

  "runtime_minutes": 45,

  "year": 2008,

  "end_year": 2013,

  "release_date": "2008-01-20",

  "imdb_id": "tt0903747",

  "tmdb_id": 1396,

  "tmdb_type": "tv",

  "genres": [7],

  "genre_names": ["Drama"],

  "user_rating": 9.2,

  "critic_score": 85,

  "us_rating": "TV-MA",

  "poster": "https://cdn.watchmode.com/posters/03173903_poster_w185.jpg",

  "backdrop": "https://cdn.watchmode.com/backdrops/03173903_bd_w780.jpg",

  "original_language": "en",

  "similar_titles": [

    316213, 3109684, 335115, 3108093, 350168, 373995, 52048, 312149, 3131957,

    3131293, 398260, 3110052

  ],

  "networks": [8],

  "network_names": ["AMC"],

  "trailer": "https://www.youtube.com/watch?v=XZ8daibM3AE",

  "trailer_thumbnail": "https://cdn.watchmode.com/video_thumbnails/536008_pthumbnail_320.jpg",

  "relevance_percentile": 98.92,

  "sources": [

    {

      "source_id": 203,

      "name": "Netflix",

      "type": "sub",

      "region": "US",

      "ios_url": "nflx://www.netflix.com/title/70143836",

      "android_url": "nflx://www.netflix.com/Browse?
      q=action%3Dplay%26source%3Dmerchweb%26target_url%3Dhttp%3A%2F%2Fmovi.es%2FVoft6",

      "web_url": "http://www.netflix.com/title/70143836",

      "format": "4K",

      "price": null,

      "seasons": 5,

      "episodes": 62

    },

    {

      "source_id": 349,

      "name": "iTunes",

      "type": "buy",

      "region": "US",

      "ios_url": "com.apple.TVShows://product/Pilot,%20Season%201/271382034/tvSeason",

      "android_url": null,

      "web_url": "https://itunes.apple.com/us/tv-season/pilot/id271383858?i=271866344&amp;uo=4&amp;
      at=1000l3V2",

      "format": "HD",

      "price": 1.99,

      "seasons": 5,

      "episodes": 62

    },

    {

      "source_id": 307,

      "name": "VUDU",

      "type": "buy",

      "region": "US",

      "ios_url": "vuduapp://play?contentId=207577",

      "android_url": "vuduapp://207577",

      "web_url": "https://www.vudu.com/content/movies/details/Breaking-Bad-Pilot/207577",

      "format": "HD",

      "price": 1.99,

      "seasons": 5,

      "episodes": 62

    }

  ]

}

### search by actor
basic info and movies they play in

{

  "id": 7110004,

  "full_name": "Brad Pitt",

  "first_name": "Brad",

  "last_name": "Pitt",

  "tmdb_id": 287,

  "imdb_id": "nm0000093",

  "main_profession": "actor",

  "secondary_profession": "producer",

  "tertiary_profession": "soundtrack",

  "date_of_birth": "1963-12-18",

  "date_of_death": null,

  "place_of_birth": "Shawnee, Oklahoma, USA",

  "gender": "m",

  "headshot_url": "https://cdn.watchmode.com/profiles/07110004_profile_185.jpg",

  "known_for": [1132806, 1336708, 1183315, 1387087],

  "relevance_percentile": 100
  
}