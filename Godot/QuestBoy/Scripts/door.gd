extends StaticBody2D
class_name Door

signal onHit(target_scene: String)

@export var target_scene : String = ""

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	add_to_group("Door")

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func _on_area_2d_body_entered(body: Node2D) -> void:
	if body.is_in_group("Player"):
		print("HIT DOOR")
		emit_signal("onHit", target_scene)
