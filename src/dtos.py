

class ClasePeliculaDTO:
    '''Este clase cumpple una función de Data Transfer Object.
    Contiene todas las propiedades del Data Set, con todos sus setters y getters.
    '''
    _html               = ""
    _movie_titles       = []
    _movie_years        = []
    _movie_countries    = []
    _movie_ratings      = []
    _movie_rating_counts= []
    _movie_directors    = []
    _movie_cast         = []
    _movie_links        = []
    _titulo_original    = []
    _duracion           = []
    _genero             = []
    _sinopsis           = []

    
    def __init__(self, html, movie_titles, movie_years, movie_countries, movie_ratings, 
                 movie_rating_counts, movie_directors, movie_cast, movie_links,
                 titulo_original, duracion, genero, sinopsis):
        self._html                  = html
        self._movie_titles          = movie_titles
        self._movie_years           = movie_years
        self._movie_countries       = movie_countries
        self._movie_ratings         = movie_ratings
        self._movie_rating_counts   = movie_rating_counts
        self._movie_directors       = movie_directors
        self._movie_cast            = movie_cast
        self._movie_links           = movie_links
        self._titulo_original       = titulo_original
        self._duracion              = duracion
        self._genero                = genero
        self._sinopsis              = sinopsis
    

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
    def get_titulo_original(self):
        return self._titulo_original
    def get_duracion(self):
        return self._duracion
    def get_genero(self):
        return self._genero
    def get_sinopsis(self):
        return self._sinopsis
    
    
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
    def set_titulo_original(self, titulo_original):
        self._titulo_original = titulo_original
    def set_duracion(self, duracion):
        self._duracion = duracion
    def set_genero(self, genero):
        self._genero = genero
    def set_sinopsis(self, sinopsis):
        self._sinopsis = sinopsis



