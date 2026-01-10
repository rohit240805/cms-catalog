import enum

class ProgramStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

class LessonStatus(str, enum.Enum):
    draft = "draft"
    scheduled = "scheduled"
    published = "published"
    archived = "archived"

class AssetVariant(str, enum.Enum):
    portrait = "portrait"
    landscape = "landscape"
    square = "square"
    banner = "banner"
    
class UserRole(str, enum.Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"
