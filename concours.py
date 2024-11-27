class selection:
    s_id: int
    stage: int
    book_id: int
    vote: int

    def __init__(self,
                 s_id: int,
                 stage: int,
                 book_id: int,
                 vote: int) -> object:
        self.vote = vote
        self.stage = stage
        self.s_id = s_id
        ''' Cette valeur ne sera pas utilisée à la création car MySQL 
        incrémente cet index (clé)'''
        self.book_id = book_id
    def __str__(self):
        return f"Selection ID: {self.s_id}, Stage: {self.stage}, Book ID: {self.book_id}, Votes: {self.vote}"