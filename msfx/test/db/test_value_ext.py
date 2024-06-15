class Value:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"

# Example usage
values = [Value("CCOMPANY"), Value("CARTICLE"), Value("QSALES")]
print(values)  # This will use the __repr__ method
