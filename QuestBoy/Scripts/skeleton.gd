extends EnemyBase
class_name Skeleton

var last_direction = Vector2(1, 0)

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
	
func _physics_process(delta: float) -> void:
	super._physics_process(delta)
	#print($AnimatedSprite2D.animation)
	
	if is_hurt or defeated:
		return
		
	if velocity.length() > 0:
		last_direction = velocity.normalized()
		if velocity.x > 0:
			$AnimatedSprite2D.play("walk_right")
		elif velocity.x < 0:
			$AnimatedSprite2D.play("walk_left")
	else:
		if last_direction.x >= 0:
			$AnimatedSprite2D.play("idle_right")
		else:
			$AnimatedSprite2D.play("idle_left")
			
func play_hurt_animation():
	if velocity.x > 0:
		$AnimatedSprite2D.play("hurt_right")
	else:
		$AnimatedSprite2D.play("hurt_left")


func _on_danger_zone_body_entered(body: Node2D) -> void:
	handle_body_entered(body)
