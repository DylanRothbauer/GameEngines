extends StaticBody2D


# Called when the node enters the scene tree for the first time.
func _ready():
	$AnimatedSprite2D.play("default")


func _on_damage_zone_body_entered(body: Node2D):
	if body.name == "Player":
		body.take_damage(1)
