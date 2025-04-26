extends GutTest

var PlayerScene = preload("res://Entities/Player.tscn")
var Axe = preload("res://Entities/axe.tscn")
var player
var player_model

func before_each():
	player = PlayerScene.instantiate()
	add_child(player)
	await get_tree().process_frame
	player_model = player.get_node("PlayerModel")
	await get_tree().process_frame
	pass
	
func after_each():
	player.queue_free()
	pass
	

# HEALTH
func test_model_initial_health():
	assert_eq(player_model.health, player_model.max_health, "Model should start at full health")

func test_model_damage():
	player.take_damage(1)  # if your model has this method
	assert_eq(player_model.health, player_model.max_health - 1, "Health should decrease by 1")
	
func test_player_takes_damage():
	player.take_damage(2)
	await get_tree().process_frame
	assert_eq(player_model.health, player_model.max_health - 2, "Player should lose 2 health")

func test_player_dies():
	player_model.health = 1
	player.take_damage(1)
	await get_tree().create_timer(1.1).timeout
	assert_true(player_model.is_dead, "Player should be dead after taking lethal damage")
	
# Test for taking damage
func test_player_takes_damage_animation():
	# Store initial health
	var initial_health = player_model.health
	
	# Take damage
	player.take_damage(1)

	# Assert that health has decreased
	assert_eq(player_model.health, initial_health - 1, "Player's health should decrease after taking damage")

	# Check if the hurt animation was played and is_hurt flag is set during animation
	await get_tree().create_timer(0.1).timeout  # Allow for animation to start
	assert_true(player_model.is_hurt, "Hurt flag should be true while taking damage")

	# Wait for the hurt animation to finish and check if is_hurt flag is reset
	await get_tree().create_timer(0.6).timeout
	assert_false(player_model.is_hurt, "Hurt flag should reset after animation ends")
	
#  Direction Tracking
func test_direction_updates_on_input():
	# simulate movement
	Input.action_press("right")
	await get_tree().process_frame
	player._physics_process(0.016)
	Input.action_release("right")

	assert_eq(player.last_direction.x, 1.0, "Last direction should be right")
	
# Shooting



# Pushback
func test_pushback_sets_timer_and_velocity():
	player.apply_pushback(Vector2(100, 0))
	assert_eq(player.pushback_velocity, Vector2(100, 0), "Pushback velocity should be set")
	assert_eq(player.pushback_timer, player.pushback_duration, "Pushback timer should initialize")
