extends Node

var next_world_path

@onready var current_world = $"../Level 1"
@onready var anim = $CanvasLayer/AnimationPlayer

var is_fading = false

func _ready() -> void:
	print("AnimationPlayer found? ", anim != null)

func _on_animation_player_animation_finished(anim_name: StringName) -> void:
	match anim_name:
		"fade_out":
			pass
		"fade_in":
			get_tree().change_scene_to_file(next_world_path)
			

			
func play_fade_in():
	anim.play("fade_in")
func play_fade_out():
	anim.play("fade_out")
	
func transition_to_scene(path: String):
	next_world_path = path
	anim.play("fade_in") # screen goes black
