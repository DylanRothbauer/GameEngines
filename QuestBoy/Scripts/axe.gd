extends Node2D

var speed = 100
var damage = 1
var direction = Vector2.ZERO

func _ready():
	$AnimatedSprite2D.play("default")
	# add_to_group("Projectile")
	
func destroy():
	queue_free()


func _physics_process(delta: float):
	global_position += (direction * speed * delta)


func _on_visible_on_screen_notifier_2d_screen_exited() -> void:
	queue_free()


func _on_body_entered(body: Node2D) -> void:
	destroy()
	
func get_damage():
	return damage
