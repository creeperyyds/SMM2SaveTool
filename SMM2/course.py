import codecs
import streams

class Course:
    def __init__(self, data=None):
        if not data:
            return None
        else:
            self.load(data)

    def load(self, data=None):
        if not data:
            return None
        else:
            self.data = data
            self.stream = streams.StreamIn(self.data)
            self.stream.byteorder = codecs.BOM_UTF16_LE
            self.HEADER = CourseHeader(self.stream.read(0x200, codecs.BOM_UTF16_BE))
            self.OVERWORLD = CourseArea(self.stream.read(0x2DEE0, codecs.BOM_UTF16_BE))
            self.SUBWORLD = CourseArea(self.stream.read(0x2DEE0, codecs.BOM_UTF16_BE))

    def save(self):
        self.stream = streams.StreamOut()
        self.stream.byteorder = codecs.BOM_UTF16_LE
        self.stream.write(self.HEADER.save())
        self.stream.write(self.OVERWORLD.save())
        self.stream.write(self.SUBWORLD.save())

class CourseHeader:
    def __init__(self, data=None):
        if not data:
            return None
        else:
            self.load(data)

    def load(self, data=None):
        if not data:
            return None
        else:
            self.data = data
            self.stream = streams.StreamIn(self.data)
            self.stream.byteorder = codecs.BOM_UTF16_LE
            self.START_POSITION = {
                "Y": self.stream.read8()
            }
            self.GOAL_POSITION = {
                "Y": self.stream.read8(),
                "X": self.stream.read16()
            }
            self.TIME_LIMIT = self.stream.read16()
            self.CC_COUNT = self.stream.read16()
            self.SAVE_DATE = {
                "YEAR": self.stream.read16(),
                "MONTH": self.stream.read8(),
                "DAY": self.stream.read8()
            }
            self.SAVE_TIME = {
                "HOUR": self.stream.read8(),
                "MINUTE": self.stream.read8()
            }
            self.AUTOSCROLL_SPEED = self.stream.read8()
            self.CC_CATEGORY = self.stream.read8()
            self.CC_HASH = self.stream.read32()
            self.GAME_VERSION = self.stream.read32()
            self.MANAGEMENT_FLAGS = self.stream.read32()
            self.CC_TRY_COUNT = self.stream.read32()
            self.CC_TIME = self.stream.read32()
            self.CREATION_ID = self.stream.read32()
            self.UPLOAD_ID = self.stream.read64()
            self.COMPLETION_FLAGS = self.stream.read32()
            self.stream.skip(0xBD)
            self.GAME_STYLE = self.stream.read(0x2)
            self.stream.skip(0x1)
            self.NAME = self.stream.read(0x42, codecs.BOM_UTF16_BE).decode("utf-16-le", errors="ignore").rstrip('\x00')
            self.DESCRIPTION = self.stream.read(0xCA, codecs.BOM_UTF16_BE).decode("utf-16-le", errors="ignore").rstrip('\x00')

    def save(self):
        self.stream = streams.StreamOut()
        self.stream.byteorder = codecs.BOM_UTF16_LE
        self.stream.write8(self.START_POSITION['Y'])
        self.stream.write8(self.GOAL_POSITION['Y'])
        self.stream.write16(self.GOAL_POSITION['X'])
        self.stream.write16(self.TIME_LIMIT)
        self.stream.write16(self.CC_COUNT)
        self.stream.write16(self.SAVE_DATE['YEAR'])
        self.stream.write8(self.SAVE_DATE['MONTH'])
        self.stream.write8(self.SAVE_DATE['DAY'])
        self.stream.write8(self.SAVE_TIME['HOUR'])
        self.stream.write8(self.SAVE_DATE['MINUTE'])
        self.stream.write8(self.AUTOSCROLL_SPEED)
        self.stream.write8(self.CC_CATEGORY)
        self.stream.write32(self.CC_HASH)
        self.stream.write32(self.GAME_VERSION)
        self.stream.write32(self.MANAGEMENT_FLAGS)
        self.stream.write32(self.CC_TRY_COUNT)
        self.stream.write32(self.CC_TIME)
        self.stream.write32(self.CREATION_ID)
        self.stream.write64(self.UPLOAD_ID)
        self.stream.write32(self.COMPLETION_FLAGS)
        self.stream.write(b'\x00' * 0xBD)
        self.stream.write(self.GAME_STYLE)
        self.stream.write(b'\x00')
        self.stream.write(self.NAME)
        self.stream.write(self.DESCRIPTION)
        self.data = self.stream.data
        return self.data

class CourseArea:
    def __init__(self, data=None):
        if not data:
            return None
        else:
            self.load(data)

    def load(self, data=None):
        if not data:
            return None
        else:
            self.data = data
            self.stream = streams.StreamIn(self.data)
            self.stream.byteorder = codecs.BOM_UTF16_LE
            self.AREA_THEME = self.stream.read8()
            self.AUTOSCROLL_TYPE = self.stream.read8()
            self.SCREEN_BOUNDARY_FLAGS = self.stream.read8()
            self.AREA_ORIENTATION = self.stream.read8()
            self.END_LIQUID_HEIGHT = self.stream.read8()
            self.LIQUID_MODE = self.stream.read8()
            self.LIQUID_SPEED = self.stream.read8()
            self.END_LIQUID_HEIGHT = self.stream.read8()
            self.BOUNDARIES = {
                "RIGHT":self.stream.read32(),
                "TOP":self.stream.read32(),
                "LEFT":self.stream.read32(),
                "BOTTOM":self.stream.read32()
            }
            self.AREA_FLAGS = self.stream.read32()
            self.ACTOR_COUNT = self.stream.read32()
            self.OTOASOBI_COUNT = self.stream.read32()
            self.SNAKE_BLOCK_COUNT = self.stream.read32()
            self.CLEAR_DOKAN_COUNT = self.stream.read32()
            self.NOBINOBI_PAKKUN_COUNT = self.stream.read32()
            self.BLOCK_BIKKURI_COUNT = self.stream.read32()
            self.ORBIT_BLOCK_COUNT = self.stream.read32()
            self.stream.skip(0x4)
            self.TILE_COUNT = self.stream.read32()
            self.RAIL_COUNT = self.stream.read32()
            self.ICICLE_COUNT = self.stream.read32()
            self.ACTOR_DATA = self.stream.substream(0x20 * 2600, codecs.BOM_UTF16_BE)
            self.OTOASOBI_DATA = self.stream.substream(0x4 * 300, codecs.BOM_UTF16_BE)
            self.SNAKE_BLOCK_DATA = self.stream.substream(0x3C4 * 5, codecs.BOM_UTF16_BE)
            self.CLEAR_DOKAN_DATA = self.stream.substream(0x124 * 200, codecs.BOM_UTF16_BE)
            self.NOBINOBI_PAKKUN_DATA = self.stream.substream(0x54 * 10, codecs.BOM_UTF16_BE)
            self.BLOCK_BIKKURI_DATA = self.stream.substream(0x2C * 10, codecs.BOM_UTF16_BE)
            self.ORBIT_BLOCK_DATA = self.stream.substream(0x2C * 10, codecs.BOM_UTF16_BE)
            self.TILE_DATA = self.stream.substream(0x4 * 4000, codecs.BOM_UTF16_BE)
            self.RAIL_DATA = self.stream.substream(0xC * 1500, codecs.BOM_UTF16_BE)
            self.ICICLE_DATA = self.stream.substream(0x4 * 300, codecs.BOM_UTF16_BE)
            self.ACTORS = []
            for i in range(self.ACTOR_COUNT):
                self.ACTORS.append(Actor(self.ACTOR_DATA.read(0x20, codecs.BOM_UTF16_BE)))

    def save(self):
        self.stream = streams.StreamOut()
        self.stream.byteorder = codecs.BOM_UTF16_LE
        self.stream.write8(self.AREA_THEME)
        self.stream.write8(self.AUTOSCROLL_TYPE)
        self.stream.write8(self.SCREEN_BOUNDARY_FLAGS)
        self.stream.write8(self.AREA_ORIENTATION)
        self.stream.write8(self.END_LIQUID_HEIGHT)
        self.stream.write8(self.LIQUID_MODE)
        self.stream.write8(self.LIQUID_SPEED)
        self.stream.write8(self.END_LIQUID_HEIGHT)
        self.stream.write32(self.BOUNDARIES['RIGHT'])
        self.stream.write32(self.BOUNDARIES['TOP'])
        self.stream.write32(self.BOUNDARIES['LEFT'])
        self.stream.write32(self.BOUNDARIES['BOTTOM'])
        self.stream.write32(self.AREA_FLAGS)
        self.stream.write32(self.ACTOR_COUNT)
        self.stream.write32(self.OTOASOBI_COUNT)
        self.stream.write32(self.SNAKE_BLOCK_COUNT)
        self.stream.write32(self.CLEAR_DOKAN_COUNT)
        self.stream.write32(self.NOBINOBI_PAKKUN_COUNT)
        self.stream.write32(self.BLOCK_BIKKURI_COUNT)
        self.stream.write32(self.ORBIT_BLOCK_COUNT)
        self.stream.write(b'\x00\x00\x00\x00')
        self.stream.write32(self.TILE_COUNT)
        self.stream.write32(self.RAIL_COUNT)
        self.stream.write32(self.ICICLE_COUNT)
        actor_stream = streams.StreamOut()
        for actor in self.ACTORS: actor_stream.write(actor.save())
        actor_stream.write(b'\x00' * (2600 - len(actor_stream.data)))
        self.ACTOR_DATA = streams.StreamIn(actor_stream.data)
        self.stream.write(actor_stream.data)
        self.stream.write(self.OTOASOBI_DATA.data)
        self.stream.write(self.SNAKE_BLOCK_DATA.data)
        self.stream.write(self.CLEAR_DOKAN_DATA.data)
        self.stream.write(self.NOBINOBI_PAKKUN_DATA.data)
        self.stream.write(self.BLOCK_BIKKURI_DATA.data)
        self.stream.write(self.ORBIT_BLOCK_DATA.data)
        self.stream.write(self.TILE_DATA.data)
        self.stream.write(self.RAIL_DATA.data)
        self.stream.write(self.ICICLE_DATA.data)
        self.data = self.stream.data
        return self.data

class Actor:
    def __init__(self, data=None):
        if not data:
            return None
        else:
            self.load(data)

    def load(self, data=None):
        if not data:
            return None
        else:
            self.data = data
            self.stream = streams.StreamIn(self.data)
            self.stream.byteorder = codecs.BOM_UTF16_LE
            self.POSITION = {
                "X":self.stream.read32(),
                "Y":self.stream.read32()
            }
            self.stream.skip(0x2)
            self.SIZE = {
                "X":self.stream.read8(),
                "Y":self.stream.read8()
            }
            self.FLAGS = [
                self.stream.read32(),
                self.stream.read32()
            ]
            self.EXTENDED_DATA = self.stream.read32()
            self.TYPES = {
                "PARENT":[
                    self.stream.read8(),
                    self.stream.read8()
                ],
                "CHILD":[
                    self.stream.read8(),
                    self.stream.read8()
                ]
            }
            self.LINK_ID = self.stream.read16()
            self.OTOASOBI_ID = self.stream.read16()

    def save(self):
        self.stream = streams.StreamOut()
        self.stream.byteorder = codecs.BOM_UTF16_LE
        self.stream.write32(self.POSITION['X'])
        self.stream.write32(self.POSITION['Y'])
        self.stream.write8(self.SIZE['X'])
        self.stream.write8(self.SIZE['Y'])
        for flag in self.FLAGS: self.stream.write32(flag)
        self.stream.write32(self.EXTENDED_DATA)
        for parent in self.TYPES['PARENT']: self.stream.write8(parent)
        for child in self.TYPES['CHILD']: self.stream.write8(child)
        self.stream.write16(self.LINK_ID)
        self.stream.write16(self.OTOASOBI_ID)
        self.data = self.stream.data
        return self.data
