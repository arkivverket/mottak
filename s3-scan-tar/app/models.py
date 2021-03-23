class AVScanResult:
    """
    Parameter class used to send the result of the avscan between functions
    """
    clean: int
    virus: int
    skipped: int

    def __init__(self, clean, virus, skipped):
        self.clean = clean
        self.virus = virus
        self.skipped = skipped

    def __eq__(self, other):
        if isinstance(other, AVScanResult):
            return self.clean == other.clean and \
                   self.virus == other.virus and \
                   self.skipped == other.skipped
        return False

    def get_status(self):
        if self.virus == 0:
            return "ok"
        else:
            return "Ikke ok"

    def get_scanned_summation(self):
        scanned = self.clean + self.virus
        total = scanned + self.skipped
        return f"{scanned} av {total}"

    def generate_message(self):
        return (
                f"Status etter virus scan: {self.get_status()}\n\n"
                f"Antall filer kontrollert: {self.get_scanned_summation()}\n"
                f"    - Filer uten virus: {self.clean}\n"
                f"    - Filer med virus: {self.virus}\n"
                f"    - Filer ikke kontrollert pga. filstørrelse: {self.skipped}"
                )
