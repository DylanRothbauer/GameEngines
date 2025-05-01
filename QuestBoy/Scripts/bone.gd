extends Node2D

var speed = 100
var damage = 1
var direction = Vector2.ZERO

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	$AnimatedSprite2D.play("default")

func destroy():
	queue_free()

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func _physics_process(delta: float):
	global_position += (direction * speed * delta)

func _on_area_2d_body_entered(body: Node2D) -> void:
	if body.is_in_group("Player"):
		body.take_damage(1)
		destroy()
		
func _on_visible_on_screen_notifier_2d_screen_exited() -> void:
	destroy()
