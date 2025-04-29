# enemy_base.gd
extends CharacterBody2D
class_name EnemyBase

signal enemy_defeated(name)

var health: int = 2
var is_hurt: bool = false
var defeated: bool = false

var pushback_velocity = Vector2.ZERO
var pushback_timer: float = 0.0
const PUSHBACK_DURATION = 0.2
const PUSHBACK_FORCE = 100.0

func _physics_process(delta: float) -> void:
	move_and_slide()
	
	# Apply pushback (optional - maybe later)
#	if pushback_timer > 0:
#		pushback_timer -= delta
#		if pushback_timer <= 0:
#			pushback_velocity = Vector2.ZERO

	if is_hurt or defeated:
		return

	if health <= 0:
		destroy()
		
	# Child animations here

func take_damage(amount: int) -> void:
	if is_hurt or defeated:
		return
	
	is_hurt = true
	health -= amount
	
	play_hurt_animation()

	await get_tree().create_timer(0.5).timeout
	is_hurt = false

func destroy() -> void:
	if defeated:
		return
	defeated = true
	emit_signal("enemy_defeated", name)
	queue_free()

func play_hurt_animation():
	# Placeholder: child classes will override
	pass
