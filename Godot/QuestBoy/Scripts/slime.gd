extends EnemyBase
class_name Slime

var last_direction = Vector2(1, 0)

func _ready():
	pass

func _physics_process(delta: float):
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

func _on_damage_zone_body_entered(body: Node2D):
	handle_body_entered(body)

func _on_damage_zone_area_entered(area: Area2D):
	handle_area_entered(area)
	
func play_hurt_animation():
	if velocity.x > 0:
		$AnimatedSprite2D.play("hurt_right")
	else:
		$AnimatedSprite2D.play("hurt_left")
		
func on_player_nearby(state_node):
	state_node.Transistioned.emit(state_node, "EnemyFollow")
