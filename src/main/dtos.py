class ClasePeliculaDTO:
    '''
    Esta clase cumple una función de Data Transfer Object (DTO).
    Contiene todas las propiedades de un conjunto de datos de películas, con sus respectivos setters y getters.
    '''
    _html                  = ""
    _movie_titles          = []
    _movie_years           = []
    _movie_countries       = []
    _movie_ratings         = []
    _movie_rating_counts   = []
    _movie_directors       = []
    _movie_cast            = []
    _movie_links           = []
    _movie_original_titles = []
    _movie_durations       = []
    _movie_genres          = []
    _movie_synopses        = []

    
    def __init__(self, html, movie_titles, movie_years, movie_countries, movie_ratings, 
                 movie_rating_counts, movie_directors, movie_cast, movie_links,
                 movie_original_titles, movie_durations, movie_genres, movie_synopses):
        self._html                  = html
        self._movie_titles          = movie_titles
        self._movie_years           = movie_years
        self._movie_countries       = movie_countries
        self._movie_ratings         = movie_ratings
        self._movie_rating_counts   = movie_rating_counts
        self._movie_directors       = movie_directors
        self._movie_cast            = movie_cast
        self._movie_links           = movie_links
        self._movie_original_titles = movie_original_titles
        self._movie_durations       = movie_durations
        self._movie_genres          = movie_genres
        self._movie_synopses        = movie_synopses
    

    # Métodos getters
    def get_html(self):
        return self._html
    def get_movie_titles(self):
        return self._movie_titles
    def get_movie_years(self):
        return self._movie_years
    def get_movie_countries(self):
        return self._movie_countries
    def get_movie_ratings(self):
        return self._movie_ratings
    def get_movie_rating_counts(self):
        return self._movie_rating_counts
    def get_movie_directors(self):
        return self._movie_directors
    def get_movie_cast(self):
        return self._movie_cast
    def get_movie_links(self):
        return self._movie_links
    def get_movie_original_titles(self):
        return self._movie_original_titles
    def get_movie_durations(self):
        return self._movie_durations
    def get_movie_genres(self):
        return self._movie_genres
    def get_movie_synopses(self):
        return self._movie_synopses
    
    
    # Métodos setters
    def set_html(self, html):
        self._html = html
    def set_movie_titles(self, movie_titles):
        self._movie_titles = movie_titles
    def set_movie_years(self, movie_years):
        self._movie_years = movie_years
    def set_movie_countries(self, movie_countries):
        self._movie_countries = movie_countries
    def set_movie_ratings(self, movie_ratings):
        self._movie_ratings = movie_ratings
    def set_movie_rating_counts(self, movie_rating_counts):
        self._movie_rating_counts = movie_rating_counts
    def set_movie_directors(self, movie_directors):
        self._movie_directors = movie_directors
    def set_movie_cast(self, movie_cast):
        self._movie_cast = movie_cast
    def set_movie_links(self, movie_links):
        self._movie_links = movie_links
    def set_movie_original_titles(self, movie_original_titles):
        self._movie_original_titles = movie_original_titles
    def set_movie_durations(self, movie_durations):
        self._movie_durations = movie_durations
    def set_movie_genres(self, movie_genres):
        self._movie_genres = movie_genres
    def set_movie_synopses(self, movie_synopses):
        self._movie_synopses = movie_synopses