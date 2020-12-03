"""Select room tags need to be centered or click to apply to all room tags in view"""
__author__='NguyenKhanhTien - khtien0107@gmail.com'
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import Transaction, XYZ, SpatialElement, SpatialElementTag
from Autodesk.Revit.DB.Architecture import Room
from rpw import ui

doc = __revit__.ActiveUIDocument.Document

def get_bbox_center_pt(bbox):
    """ Returns center XYZ of BoundingBox Element"""
    avg_x = (bbox.Min.X + bbox.Max.X) / 2
    avg_y = (bbox.Min.Y + bbox.Max.Y) / 2
    return XYZ(avg_x, avg_y, 0)

active_view = doc.ActiveView
selection = ui.Selection()
if selection:
    room_tags = selection
else:
    room_tags = FilteredElementCollector(doc, doc.ActiveView.Id)\
        .OfClass(SpatialElementTag).ToElements()

transaction = Transaction(doc, 'Move Room Tags and Room Points to Room Center')
transaction.Start()
for room_tag in room_tags:
    room_tag_pt = room_tag.Location.Point
    room = room_tag.Room
    bou=room.get_BoundingBox(active_view)
    room_center=get_bbox_center_pt(bou)
    if (room.IsPointInRoom(room_center)):
        translation_room_tag = room_center - room_tag_pt
        room_tag.Location.Move(translation_room_tag)
transaction.Commit()