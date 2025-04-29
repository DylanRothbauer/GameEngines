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
	if body.name == "Player":
		var dir = (global_position - body.global_position).normalized()
		pushback_velocity = dir * PUSHBACK_FORCE
		pushback_timer = PUSHBACK_DURATION
		body.take_damage(1)

func _on_damage_zone_area_entered(area: Area2D):
	print("Damage zone entered")
	print("ISHURT = ", is_hurt)
	print("DEFEATED = ", defeated)
	
	if is_hurt or defeated:
		return
		
	var axe = area.get_parent()
	if axe.is_in_group("Projectile"):
		take_damage(1)
	
func play_hurt_animation():
	print("Hurt animation called")
	
	if velocity.x > 0:
		$AnimatedSprite2D.play("hurt_right")
	else:
		$AnimatedSprite2D.play("hurt_left")
		
