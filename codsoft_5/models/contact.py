class Contact:
    def __init__(self, id=None, name="", phone="", email="", address="", notes="", 
                 company="", position="", birthday="", profile_image=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.notes = notes
        self.company = company
        self.position = position
        self.birthday = birthday
        self.profile_image = profile_image
    
    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'notes': self.notes,
            'company': self.company,
            'position': self.position,
            'birthday': self.birthday,
            'profile_image': self.profile_image
        }