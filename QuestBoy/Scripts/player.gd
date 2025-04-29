extends CharacterBody2D

var last_direction = Vector2(1,0)
var prev_direction = Vector2(1,0)

var axe = preload("res://Entities/axe.tscn")
var pushback_velocity = Vector2.ZERO
var pushback_duration = 0.2
var pushback_timer = 0.0
var shoot_disabled = false

func _ready():
	$AnimatedSprite2D.play("idle_right")
	GameState.player = self
	
	# Set health from GameState
	$PlayerModel.health = GameState.player_health
	$PlayerModel.max_health = GameState.player_max_health
	
	GameState.notify_health_change($PlayerModel.health)
	
func _process(_delta: float) -> void:
		pass
	
func _physics_process(_delta: float):
	if $PlayerModel.is_hurt:
		return
	if $PlayerModel.is_dead:
		return
	
	var direction = Input.get_vector("left", "right", "up", "down")
	velocity = direction * $PlayerModel.max_speed
	move_and_slide()
	
	if Input.is_action_just_pressed("shoot"):
		shoot()
		
	if direction.length() > 0:
		last_direction = direction
		play_walk_animation(direction)
	else:
		play_idle_animation(last_direction)
		
		
func play_walk_animation(direction):
	if direction.x > 0:
		prev_direction = direction
		$AnimatedSprite2D.play("walk_right")
	elif direction.x < 0:
		prev_direction = direction
		$AnimatedSprite2D.play("walk_left")
	elif direction.y > 0:
		if prev_direction.x > 0:
			$AnimatedSprite2D.play("walk_right")
		elif prev_direction.x < 0:
			$AnimatedSprite2D.play("walk_left")
	elif direction.y < 0:
		if prev_direction.x > 0:
			$AnimatedSprite2D.play("walk_right")
		elif prev_direction.x < 0:
			$AnimatedSprite2D.play("walk_left")
		
func play_idle_animation(direction):
	if direction.x > 0:
		$AnimatedSprite2D.play("idle_right")
	elif direction.x < 0:
		$AnimatedSprite2D.play("idle_left")
	elif direction.y > 0:
		if prev_direction.x > 0:
			$AnimatedSprite2D.play("idle_right")
		elif prev_direction.x < 0:
			$AnimatedSprite2D.play("idle_left")
	elif direction.y < 0:
		if prev_direction.x > 0:
			$AnimatedSprite2D.play("idle_right")
		elif prev_direction.x < 0:
			$AnimatedSprite2D.play("idle_left")
			
func play_dead_animation():
	print("Dead animation triggered")
	if $PlayerModel.is_dead:
		return
		
	$PlayerModel.is_dead = true
	$AnimatedSprite2D.play("die")
	await get_tree().create_timer(1.0).timeout
	
func play_hurt_animation():
	if $PlayerModel.is_hurt:
		return
		
	$PlayerModel.is_hurt = true
	
	if last_direction.x >= 0:
		$AnimatedSprite2D.play("hurt_right")
	else:
		$AnimatedSprite2D.play("hurt_left")
		
	await get_tree().create_timer(0.5).timeout  # Let the animation finish
	$PlayerModel.is_hurt = false
			
func take_damage(value):
	
	if $PlayerModel.is_dead:
		return
		
	$PlayerModel.health -= value
	GameState.player_health = $PlayerModel.health
	GameState.notify_health_change($PlayerModel.health) # Signal
	
	# $"../HUD/Health".update_health($PlayerModel.health)
	
	print("PLAYER TOOK DAMAGE")
	print("HEALTH: " + str($PlayerModel.health))
	
	
	if $PlayerModel.health <= 0:
		play_dead_animation()
	else:
		play_hurt_animation()
		
func shoot():
	if shoot_disabled:
		return
	
	shoot_disabled = true
	
	if axe:
		var axe_instance = axe.instantiate()
		
		var dir = Vector2.RIGHT if prev_direction.x >= 0 else Vector2.LEFT
		dir = dir.normalized()
		
		var offset = dir * 16
		axe_instance.global_position = global_position + offset
		axe_instance.direction = dir
		
		get_tree().current_scene.add_child(axe_instance)
		
		await get_tree().create_timer(0.5).timeout
		shoot_disabled = false
