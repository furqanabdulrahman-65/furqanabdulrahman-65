from PIL import Image

# Character ramp (light → dark)
ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

WIDTH = 110


class AsciiGenerator:

    def __init__(self, image_path):
        self.image = Image.open(image_path).convert("L")

    def resize(self):

        w, h = self.image.size

        ratio = h / w

        new_height = int(WIDTH * ratio * 0.55)

        self.image = self.image.resize((WIDTH, new_height))

    def pixels_to_ascii(self):

        pixels = self.image.getdata()

        chars = ""

        for p in pixels:

            chars += ASCII_CHARS[p * (len(ASCII_CHARS)-1)//255]

        return chars

    def generate(self):

        self.resize()

        chars = self.pixels_to_ascii()

        width = self.image.width

        rows = []

        for i in range(0, len(chars), width):

            rows.append(chars[i:i+width])

        return rows


if __name__ == "__main__":

    generator = AsciiGenerator("source-prepped.png")

    rows = generator.generate()

    with open("ascii.txt","w",encoding="utf8") as f:

        for r in rows:

            f.write(r+"\n")

    print("ASCII generated.")