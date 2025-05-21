extends State
class_name EnemyFollow

@export var enemy : CharacterBody2D
@export var move_speed := 30.0

var player : CharacterBody2D

func Enter():
	player = get_tree().get_first_node_in_group("Player")
	
func Physics_Update(delta : float):

	# var direction = player.global_position - enemy.global_position
	# var distance = direction.length()
	
#	if enemy.pushback_timer > 0:
#		enemy.pushback_timer -= delta
#		enemy.velocity = enemy.pushback_velocity
#		return

	var direction = player.global_position - enemy.global_position
	var distance = direction.length()

	# Keep chasing unless directly colliding with player
	if distance > 10:
		enemy.velocity = direction.normalized() * move_speed
	else:
		enemy.velocity = Vector2()

	# Only go idle if player runs far away
	if distance > 100:
		Transistioned.emit(self, "EnemyIdle")
