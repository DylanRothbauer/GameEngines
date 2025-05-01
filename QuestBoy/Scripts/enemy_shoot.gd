extends State
class_name EnemyShoot

@export var enemy: CharacterBody2D
@export var shoot_range := 120.0
@export var shoot_cooldown := 1.5
@export var projectile_scene: PackedScene  # Assign any projectile (bone, fireball, etc.)

var player: CharacterBody2D
var time_since_last_shot := 0.0

func Enter():
	player = get_tree().get_first_node_in_group("Player")
	time_since_last_shot = shoot_cooldown  # shoot immediately

func Update(delta: float) -> void:
	if not player or not enemy:
		return

	time_since_last_shot += delta
	var to_player = player.global_position - enemy.global_position

	if to_player.length() > shoot_range:
		Transistioned.emit(self, "EnemyIdle")  # Exit shooting state
		return

	if time_since_last_shot >= shoot_cooldown:
		shoot_projectile(to_player.normalized())
		time_since_last_shot = 0.0

func shoot_projectile(direction: Vector2):
	if not projectile_scene:
		push_error("No projectile_scene assigned in EnemyShoot.")
		return

	var projectile = projectile_scene.instantiate()
	projectile.position = enemy.global_position
	projectile.direction = direction  # Your projectile script should expose this
	get_tree().current_scene.add_child(projectile)
