class ClasePeliculaDTO:

    _html = ""
    _movie_links = []
    
    def __init__(self, html, movie_links):
        self._html = html
        self._movie_links = movie_links
    

    # Métodos getters
    def get_html(self):
        return self._html
    
    def get_movie_links(self):
        return self._movie_links
    
    
    # Métodos setters
    def set_html(self, html):
        self._html = html

    def set_movie_links(self, movie_links):
        self._movie_links = movie_links