extends CharacterBody2D
class_name Slime

signal slime_defeated(name)

var last_direction = Vector2(1, 0)
var health = 2
var is_hurt = false
var defeated = false

var pushback_velocity = Vector2.ZERO
var pushback_timer = 0.0
const PUSHBACK_DURATION = 0.2
const PUSHBACK_FORCE = 100.0

func _physics_process(delta: float):
	move_and_slide()
	if is_hurt or defeated:
		return

	if health <= 0:
		destroy()

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

func destroy():
	if defeated:
		return  # Already handled
	defeated = true
	emit_signal("slime_defeated", name)
	queue_free()

func is_defeated() -> bool:
	return defeated

func _on_damage_zone_body_entered(body: Node2D):
	if body.name == "Player":
		var dir = (global_position - body.global_position).normalized()
		pushback_velocity = dir * PUSHBACK_FORCE
		pushback_timer = PUSHBACK_DURATION
		body.take_damage(1)

func _on_damage_zone_area_entered(area: Area2D):
	if is_hurt or defeated:
		return

	is_hurt = true
	var axe = area.get_parent()
	if axe.is_in_group("Projectile"):
		health -= 1
		if velocity.x > 0:
			$AnimatedSprite2D.play("hurt_right")
		else:
			$AnimatedSprite2D.play("hurt_left")
	await get_tree().create_timer(0.5).timeout
	is_hurt = false
