
import os
from io import BytesIO
import shutil
from pathlib import Path
import re
from random import Random
from collections import OrderedDict
import hashlib
import yaml

from fs_helpers import *
from wwlib.yaz0 import Yaz0
from wwlib.rarc import RARC
from wwlib.dol import DOL
from wwlib.rel import REL, RELRelocation, RELRelocationType
from wwlib.gcm import GCM
from wwlib.jpc import JPC
import tweaks
from asm import patcher
from logic.logic import Logic
from paths import DATA_PATH, ASM_PATH, RANDO_ROOT_PATH, IS_RUNNING_FROM_SOURCE
import customizer
from wwlib import stage_searcher
from asm import disassemble

	
									
				   
			   

from randomizers import items
from randomizers import charts
from randomizers import starting_island
from randomizers import entrances
# from randomizers import music
from randomizers import enemies
from randomizers import palettes

with open(os.path.join(RANDO_ROOT_PATH, "version.txt"), "r") as f:
  VERSION = f.read().strip()

VERSION_WITHOUT_COMMIT = VERSION

# Try to add the git commit hash to the version number if running from source.
if IS_RUNNING_FROM_SOURCE:
						  
				   
  version_suffix = "_NOGIT"
  
  git_commit_head_file = os.path.join(RANDO_ROOT_PATH, ".git", "HEAD")
  if os.path.isfile(git_commit_head_file):
    with open(git_commit_head_file, "r") as f:
      head_file_contents = f.read().strip()
    if head_file_contents.startswith("ref: "):
      # Normal head, HEAD file has a reference to a branch which contains the commit hash
      relative_path_to_hash_file = head_file_contents[len("ref: "):]
      path_to_hash_file = os.path.join(RANDO_ROOT_PATH, ".git", relative_path_to_hash_file)
      if os.path.isfile(path_to_hash_file):
        with open(path_to_hash_file, "r") as f:
          hash_file_contents = f.read()
        version_suffix = "_" + hash_file_contents[:7]
    elif re.search(r"^[0-9a-f]{40}$", head_file_contents):
      # Detached head, commit hash directly in the HEAD file
      version_suffix = "_" + head_file_contents[:7]
  
  VERSION += version_suffix

CLEAN_WIND_WAKER_ISO_MD5 = 0xd8e4d45af2032a081a0f446384e9261b

class TooFewProgressionLocationsError(Exception):
  pass

class InvalidCleanISOError(Exception):
  pass

class Randomizer:
  def __init__(self, seed, clean_iso_path, randomized_output_folder, options, permalink=None, cmd_line_args=OrderedDict()):
    self.randomized_output_folder = randomized_output_folder
    self.options = options
    self.seed = seed
    self.permalink = permalink
    
    self.dry_run = ("-dry" in cmd_line_args)
    self.disassemble = ("-disassemble" in cmd_line_args)
    self.export_disc_to_folder = ("-exportfolder" in cmd_line_args)
    self.no_logs = ("-nologs" in cmd_line_args)
    self.bulk_test = ("-bulk" in cmd_line_args)
    if self.bulk_test:
      self.dry_run = True
      self.no_logs = True
    self.print_used_flags = ("-printflags" in cmd_line_args)
															
																	
								  
		 
								 
													 
    
	
							  
								
								   
						  
											
																					  
	
						   
													   
							 
    self.integer_seed = self.convert_string_to_integer_md5(self.seed)
    self.rng = self.get_new_rng()
    
    self.arcs_by_path = {}
    self.jpcs_by_path = {}
    self.rels_by_path = {}
    self.symbol_maps_by_path = {}
    self.raw_files_by_path = {}
    self.used_actor_ids = list(range(0x1F6))
    
    self.read_text_file_lists()
    
    if not self.dry_run:
      if not os.path.isfile(clean_iso_path):
        raise InvalidCleanISOError("Clean WW ISO does not exist: %s" % clean_iso_path)
      
      self.verify_supported_version(clean_iso_path)
      
      self.gcm = GCM(clean_iso_path)
      self.gcm.read_entire_disc()
      
      dol_data = self.gcm.read_file_data("sys/main.dol")
      self.dol = DOL()
      self.dol.read(dol_data)
      
      try:
        self.chart_list = self.get_arc("files/res/Msg/fmapres.arc").get_file("cmapdat.bin")
      except (InvalidOffsetError, AssertionError):
        # An invalid offset error when reading fmapres.arc seems to happen when the user has a corrupted clean ISO.
        # Alternatively, fmapres.arc's magic bytes not being RARC can also happen here, also caused by a corrupted clean ISO.
        # The reason for this is unknown, but when this happens check the ISO's MD5 and if it's wrong say so in an error message.
        self.verify_correct_clean_iso_md5(clean_iso_path)
        
        # But if the ISO's MD5 is correct just raise the normal offset error.
        raise
      
      self.bmg = self.get_arc("files/res/Msg/bmgres.arc").get_file("zel_00.bmg")
      
      if self.disassemble:
        self.disassemble_all_code()
      if self.print_used_flags:
        stage_searcher.print_all_used_item_pickup_flags(self)
        stage_searcher.print_all_used_chest_open_flags(self)
        stage_searcher.print_all_event_flags_used_by_stb_cutscenes(self)
																		
	
																									   
						   
				   
					   
						
						
					  
					
	 
																
	
															
													 
								   
																						   
												 
															 

													 
								  
												  

												   
								 
												   
	
																					
											 
																		 
																	 
																			
															   
													   
	  
																	
																						 
																			 
																			 
																	
																				   
																			 
																			   
																						   
																				 
																				   
																			 
																						 
																								
																		 
																				 
																		   
																						 
																				   
																		 
	  
														  
													 
										  
												 
										   
								   
	  
																 
																			 
																 
																 
																 
																	   
																 
																   
																			   
																	 
																	   
																 
																		   
																				 
															 
																	 
															   
																			 
																	   
															 
	  
	
																				   
								   
	
									 
													
							   
							  
							   
							  
							   
							  
							   
							   
							   
								
								
								
								
								
							   
							   
								
								
							   
								
								
								
							   
								
							   
								
								
							   
								
								
							   
							   
							   
								
								
								
								
								
							   
								
								
							   
							   
							   
								
							   
								
								
								
	  
	
																									  
														  
										  
																				
														  
										 
																									  
														  
										
    self.custom_model_name = "Link"
    self.using_custom_sail_texture = False
										  
	
							
	
																	   
															   
													
																					  
																		
																								 
																																					 
														  
	
																						  
																												   
																																					   
																																						  
																	
																									 
											 
									 
		 
									  
																					   
	
																				
																																	 
																															  
															
																									 
											 
											   
		 
												
  
  def randomize(self):
    options_completed = 0
    yield("Modifying game code...", options_completed)
    
    customizer.decide_on_link_model(self)
										 
    if not self.dry_run:
      self.apply_necessary_tweaks()
      
	  
										
      if self.options.get("instant_text_boxes"):
        tweaks.make_all_text_instant(self)
      if self.options.get("reveal_full_sea_chart"):
        patcher.apply_patch(self, "reveal_sea_chart")
													 
																 
      if self.options.get("invert_camera_x_axis"):
        patcher.apply_patch(self, "invert_camera_x_axis")
      if self.options.get("swift_sail"):
        tweaks.make_sail_behave_like_swift_sail(self)
      if self.options.get("increase_player_movement_speeds"):
        tweaks.increase_player_movement_speeds(self)
      if self.options.get("increase_grapple_animation_speed"):
													   
        tweaks.increase_grapple_animation_speed(self)
      if self.options.get("increase_block_moving_animation"):
        tweaks.increase_block_moving_animation(self)
      if self.options.get("increase_misc_animations"):
        tweaks.increase_misc_animations(self)
      if self.options.get("tingle_chests_without_tuner"):
        patcher.apply_patch(self, "tingle_chests_without_tuner")
      if self.options.get("KORL_control"):
        patcher.apply_patch(self, "KORL_control")
      if self.options.get("song_no_replay"):
        patcher.apply_patch(self, "song_no_replay")
      if self.options.get("swing_turn"):
        patcher.apply_patch(self, "swing_turn")
      if self.options.get("remove_title_and_ending_videos"):
        tweaks.remove_title_and_ending_videos(self)
												   
        patcher.apply_patch(self, "skipintro")
        patcher.apply_patch(self, "misc_rando_features")
        patcher.apply_patch(self, "fix_vanilla_bugs")
    
      if self.options.get("randomize_enemy_palettes"):
        yield("Choosing random enemy colors...", options_completed)
        palettes.randomize_enemy_palettes(self)

    
      if self.options.get("ballad"):
        patcher.apply_patch(self, "ballad")
      if self.options.get("titlelogo"):
        tweaks.modify_title_screen_logo(self)
      if self.options.get("memorylogo"):
        tweaks.update_game_banners(self)
										
	  
										 
							  
						  
	
											  
      if self.options.get("brisk_sail"):
        tweaks.make_sail_behave_like_brisk_sail(self)
								   
      if self.options.get("brisk_sail2"):
        tweaks.make_sail_behave_like_brisk_sail2(self)
													 
      if self.options.get("swift_sail2"):
        tweaks.make_sail_behave_like_swift_sail2(self)
		
      if self.options.get("normal_sail2"):
        tweaks.normal_sail_wind(self)
		
		


    
	
										   
								 
    options_completed += 1
    yield("Patching...", options_completed)
    
	
																																				
											 
																
									 
	
													
															 
											 
							 
	
																										
								 
	
													
							
								 
    options_completed += 2
						  
	
											   
												 
									 
	
						
    options_completed += 7
    yield("Saving patched ISO...", options_completed)
    
	
    if not self.dry_run:
      self.save_randomized_iso()
    
    options_completed += 9
						  
    
	
							
															 
								
								  
    yield("Done", -1)
  
  def apply_necessary_tweaks(self):
    patcher.apply_patch(self, "custom_funcs")
    patcher.apply_patch(self, "necessary_fixes")
													
												 
														
												 
													
    #tweaks.skip_wakeup_intro_and_start_at_dock(self)
    #tweaks.add_inter_dungeon_warp_pots(self)
									 
    # tweaks.make_all_text_instant(self)
    # tweaks.b_skips(self)
    # tweaks.modify_title_screen_logo(self)
    # tweaks.make_sail_behave_like_swift_sail(self)
									   
											 
															 
														
													 
									
    tweaks.update_game_name_icon_and_banners(self)
												  
													   
														 
										
									 
									 
												 
									
											
    # tweaks.increase_player_movement_speeds(self)
												
    # tweaks.increase_grapple_animation_speed(self)
    # tweaks.increase_block_moving_animation(self)
    # tweaks.increase_misc_animations(self)
										 
											
										
							   
											   
													
    tweaks.make_tingle_statue_reward_rupee_rainbow_colored(self)
																
													
										   
								  
													 
												   
												 
											
																
													
								 
												   
										 
											   
																 
									
    customizer.replace_link_model(self)
    tweaks.change_starting_clothes(self)
    tweaks.check_hide_ship_sail(self)
    customizer.change_player_clothes_color(self)
  
  
													  
							
												
											
												
																		  
													  
											   
																											 
													
  def verify_supported_version(self, clean_iso_path):
    with open(clean_iso_path, "rb") as f:
      game_id = try_read_str(f, 0, 6)
    if game_id != "GZLE01":
      if game_id and game_id.startswith("GZL"):
        raise InvalidCleanISOError("Invalid version of Wind Waker. Only the USA version is supported by this randomizer.")
      else:
        raise InvalidCleanISOError("Invalid game given as the clean ISO. You must specify a Wind Waker ISO (USA version).")
  
  def verify_correct_clean_iso_md5(self, clean_iso_path):
    md5 = hashlib.md5()
    
    with open(clean_iso_path, "rb") as f:
      while True:
        chunk = f.read(1024*1024)
        if not chunk:
          break
        md5.update(chunk)
    
    integer_md5 = int(md5.hexdigest(), 16)
    if integer_md5 != CLEAN_WIND_WAKER_ISO_MD5:
      raise InvalidCleanISOError("Invalid clean Wind Waker ISO. Your ISO may be corrupted.\n\nCorrect ISO MD5 hash: %x\nYour ISO's MD5 hash: %x" % (CLEAN_WIND_WAKER_ISO_MD5, integer_md5))
  
  def read_text_file_lists(self):
    # Get item names.
    self.item_names = {}
    self.item_name_to_id = {}
    with open(os.path.join(DATA_PATH, "item_names.txt"), "r") as f:
      matches = re.findall(r"^([0-9a-f]{2}) - (.+)$", f.read(), re.IGNORECASE | re.MULTILINE)
    for item_id, item_name in matches:
      if item_name:
        item_id = int(item_id, 16)
        self.item_names[item_id] = item_name
        if item_name in self.item_name_to_id:
          raise Exception("Duplicate item name: " + item_name)
        self.item_name_to_id[item_name] = item_id
    
    # Get stage and island names for debug purposes.
    self.stage_names = {}
    with open(os.path.join(DATA_PATH, "stage_names.txt"), "r") as f:
      while True:
        stage_folder = f.readline()
        if not stage_folder:
          break
        stage_name = f.readline()
        self.stage_names[stage_folder.strip()] = stage_name.strip()
    self.island_names = {}
    self.island_number_to_name = {}
    self.island_name_to_number = {}
    with open(os.path.join(DATA_PATH, "island_names.txt"), "r") as f:
      while True:
        room_arc_name = f.readline()
        if not room_arc_name:
          break
        island_name = f.readline().strip()
        self.island_names[room_arc_name.strip()] = island_name
        island_number = int(re.search(r"Room(\d+)", room_arc_name).group(1))
        self.island_number_to_name[island_number] = island_name
        self.island_name_to_number[island_name] = island_number
    
    self.item_ids_without_a_field_model = []
    with open(os.path.join(DATA_PATH, "items_without_field_models.txt"), "r") as f:
      matches = re.findall(r"^([0-9a-f]{2}) ", f.read(), re.IGNORECASE | re.MULTILINE)
    for item_id in matches:
      if item_name:
        item_id = int(item_id, 16)
        self.item_ids_without_a_field_model.append(item_id)
    
    self.arc_name_pointers = {}
    with open(os.path.join(DATA_PATH, "item_resource_arc_name_pointers.txt"), "r") as f:
      matches = re.findall(r"^([0-9a-f]{2}) ([0-9a-f]{8}) ", f.read(), re.IGNORECASE | re.MULTILINE)
    for item_id, arc_name_pointer in matches:
      item_id = int(item_id, 16)
      arc_name_pointer = int(arc_name_pointer, 16)
      self.arc_name_pointers[item_id] = arc_name_pointer
    
    self.icon_name_pointer = {}
    with open(os.path.join(DATA_PATH, "item_resource_icon_name_pointers.txt"), "r") as f:
      matches = re.findall(r"^([0-9a-f]{2}) ([0-9a-f]{8}) ", f.read(), re.IGNORECASE | re.MULTILINE)
    for item_id, icon_name_pointer in matches:
      item_id = int(item_id, 16)
      icon_name_pointer = int(icon_name_pointer, 16)
      self.icon_name_pointer[item_id] = icon_name_pointer
    
							
    with open(os.path.join(ASM_PATH, "custom_symbols.txt"), "r") as f:
      self.custom_symbols = yaml.safe_load(f)
    self.main_custom_symbols = self.custom_symbols["sys/main.dol"]
    
    with open(os.path.join(ASM_PATH, "free_space_start_offsets.txt"), "r") as f:
      self.free_space_start_offsets = yaml.safe_load(f)
    
    with open(os.path.join(DATA_PATH, "progress_item_hints.txt"), "r") as f:
      self.progress_item_hints = yaml.safe_load(f)
    
    with open(os.path.join(DATA_PATH, "island_name_hints.txt"), "r") as f:
      self.island_name_hints = yaml.safe_load(f)
    
    with open(os.path.join(DATA_PATH, "enemy_types.txt"), "r") as f:
      self.enemy_types = yaml.safe_load(f)
    
    with open(os.path.join(DATA_PATH, "palette_randomizable_files.txt"), "r") as f:
      self.palette_randomizable_files = yaml.safe_load(f)
  
  def get_arc(self, arc_path):
    arc_path = arc_path.replace("\\", "/")
    
    if arc_path in self.arcs_by_path:
      return self.arcs_by_path[arc_path]
    else:
      data = self.gcm.read_file_data(arc_path)
      arc = RARC()
      arc.read(data)
      self.arcs_by_path[arc_path] = arc
      return arc
  
  def get_jpc(self, jpc_path):
    jpc_path = jpc_path.replace("\\", "/")
    
    if jpc_path in self.jpcs_by_path:
      return self.jpcs_by_path[jpc_path]
    else:
      data = self.gcm.read_file_data(jpc_path)
      jpc = JPC(data)
      self.jpcs_by_path[jpc_path] = jpc
      return jpc
  
  def get_rel(self, rel_path):
    rel_path = rel_path.replace("\\", "/")
    
    if rel_path in self.rels_by_path:
      return self.rels_by_path[rel_path]
    else:
      if not rel_path.startswith("files/rels/"):
        raise Exception("Invalid REL path: %s" % rel_path)
      
      rel_name = os.path.basename(rel_path)
      rels_arc = self.get_arc("files/RELS.arc")
      rel_file_entry = rels_arc.get_file_entry(rel_name)
      
      if rel_file_entry:
        rel_file_entry.decompress_data_if_necessary()
        data = rel_file_entry.data
      else:
        data = self.gcm.read_file_data(rel_path)
      
      rel = REL()
      rel.read(data)
      self.rels_by_path[rel_path] = rel
      return rel
  
  def get_symbol_map(self, map_path):
    map_path = map_path.replace("\\", "/")
    
    if map_path in self.symbol_maps_by_path:
      return self.symbol_maps_by_path[map_path]
    else:
      data = self.gcm.read_file_data(map_path)
      map_text = read_all_bytes(data).decode("ascii")
      
      if map_path == "files/maps/framework.map":
        addr_to_name_map = disassemble.get_main_symbols(map_text)
      else:
        rel_name = os.path.splitext(os.path.basename(map_path))[0]
        rel = self.get_rel("files/rels/%s.rel" % rel_name)
        addr_to_name_map = disassemble.get_rel_symbols(rel, map_text)
      
      symbol_map = {}
      for address, name in addr_to_name_map.items():
        symbol_map[name] = address
      
      self.symbol_maps_by_path[map_path] = symbol_map
      return symbol_map
  
  def get_raw_file(self, file_path):
    file_path = file_path.replace("\\", "/")
    
    if file_path in self.raw_files_by_path:
      return self.raw_files_by_path[file_path]
    else:
      if file_path.startswith("files/rels/"):
        raise Exception("Cannot read a REL as a raw file.")
      elif file_path == "sys/main.dol":
        raise Exception("Cannot read the DOL as a raw file.")
	 
		
      
	  
			  
		  
	 
      data = self.gcm.read_file_data(file_path)
      
      if try_read_str(data, 0, 4) == "Yaz0":
        data = Yaz0.decompress(data)
      
      self.raw_files_by_path[file_path] = data
      return data
  
  def replace_arc(self, arc_path, new_data):
    if arc_path not in self.gcm.files_by_path:
      raise Exception("Cannot replace RARC that doesn't exist: " + arc_path)
    
    arc = RARC()
    arc.read(new_data)
    self.arcs_by_path[arc_path] = arc
  
  def replace_raw_file(self, file_path, new_data):
    if file_path not in self.gcm.files_by_path:
      raise Exception("Cannot replace file that doesn't exist: " + file_path)
    
    self.raw_files_by_path[file_path] = new_data
  
  def add_new_raw_file(self, file_path, new_data):
    if file_path.lower() in self.gcm.files_by_path_lowercase:
      raise Exception("Cannot add a new file that has the same path and name as an existing one: " + file_path)
    
    self.gcm.add_new_file(file_path, new_data)
    self.raw_files_by_path[file_path] = new_data
  
  def add_new_rel(self, rel_path, new_rel, section_index_of_actor_profile, offset_of_actor_profile):
    if not rel_path.startswith("files/rels/"):
      raise Exception("Cannot add a new REL to a folder besides files/rels/: " + rel_path)
    if rel_path.lower() in self.gcm.files_by_path_lowercase:
      raise Exception("Cannot add a new REL that has the same name as an existing one: " + rel_path)
    
    # Read the actor ID out of the actor profile.
    section_data_actor_profile = new_rel.sections[section_index_of_actor_profile].data
    new_actor_id = read_u16(section_data_actor_profile, offset_of_actor_profile+8)
    
    if new_actor_id in self.used_actor_ids:
      raise Exception("Cannot add a new REL with an actor ID that is already used:\nActor ID: %03X\nNew REL path: %s" % (new_actor_id, rel_path))
    
    # We need to add the new REL to the profile list.
    profile_list = self.get_rel("files/rels/f_pc_profile_lst.rel")
    
    rel_relocation = RELRelocation()
    rel_relocation.relocation_type = RELRelocationType.R_PPC_ADDR32
    
    rel_relocation.curr_section_num = 4 # List section
    rel_relocation.relocation_offset = new_actor_id*4 # Offset in the list
    
    # Write a null placeholder for the pointer to the profile that will be relocated.
    list_data = profile_list.sections[rel_relocation.curr_section_num].data
    write_u32(list_data, new_actor_id*4, 0)
    # For some reason, there's an extra four 0x00 bytes after the last entry in the list, so we put that there just to be safe.
    write_u32(list_data, new_actor_id*4+4, 0)
    
    rel_relocation.section_num_to_relocate_against = section_index_of_actor_profile
    rel_relocation.symbol_address = offset_of_actor_profile
    
    if new_rel.id in profile_list.relocation_entries_for_module:
      raise Exception("Cannot add a new REL with a unique ID that is already present in the profile list:\nREL ID: %03X\nNew REL path: %s" % (new_rel.id, rel_path))
    
    profile_list.relocation_entries_for_module[new_rel.id] = [rel_relocation]
    
    # Then add the REL to the game's filesystem.
    self.gcm.add_new_file(rel_path)
    self.rels_by_path[rel_path] = new_rel
    
    # Don't allow this actor ID to be used again by any more custom RELs we add.
    self.used_actor_ids.append(new_actor_id)
  
  def save_randomized_iso(self):
    self.bmg.save_changes()
    
	   
    for file_path, data in self.raw_files_by_path.items():
      self.gcm.changed_files[file_path] = data
    
    self.dol.save_changes()
    self.gcm.changed_files["sys/main.dol"] = self.dol.data
    
    for rel_path, rel in self.rels_by_path.items():
      rel.save_changes(preserve_section_data_offsets=True)
	  
      
      rel_name = os.path.basename(rel_path)
      rels_arc = self.get_arc("files/RELS.arc")
      rel_file_entry = rels_arc.get_file_entry(rel_name)
      if rel_file_entry:
        # The REL already wrote to the same BytesIO object as the file entry uses, so no need to do anything more here.
        assert rel_file_entry.data == rel.data
      else:
        self.gcm.changed_files[rel_path] = rel.data
    
    for arc_path, arc in self.arcs_by_path.items():
      for file_name, instantiated_file in arc.instantiated_object_files.items():
        if file_name == "event_list.dat":
          instantiated_file.save_changes()
      
      arc.save_changes()
      self.gcm.changed_files[arc_path] = arc.data
    
    for jpc_path, jpc in self.jpcs_by_path.items():
      jpc.save_changes()
      self.gcm.changed_files[jpc_path] = jpc.data
    
    if self.export_disc_to_folder:
      output_folder_path = os.path.join(self.randomized_output_folder, "%s" % self.seed)
      self.gcm.export_disc_to_folder_with_changed_files(output_folder_path)
    else:
      output_file_path = os.path.join(self.randomized_output_folder, "%s.iso" % self.seed)
      self.gcm.export_disc_to_iso_with_changed_files(output_file_path)
  
  def convert_string_to_integer_md5(self, string):
    return int(hashlib.md5(string.encode('utf-8')).hexdigest(), 16)
  
  def get_new_rng(self):
    rng = Random()
    rng.seed(self.integer_seed)
    if self.options.get("do_not_generate_spoiler_log"):
      for i in range(1, 100):
        rng.getrandbits(i)
    return rng
			  
  
													  
							
	
					   
										
						 
										
												   
	  
																	   
								  
										   
													 
	   
									  
																  
	  
	  
										   
																															 
														 
												 
															  
		 
												
																	  
																				   
		 
												
																			  
																						   
												   
			
										   
		  
																				 
																												  
	  
	  
													
																 
												 
																  
	  
						   
																					 
						 
																					   
	  
															   
	  
																			
										   
				  
									   
																	   
																										 
																				 
														  
	  
															
	
						 
																															  
																				   
					   
												
														  
		  
															
	
							  
  
						   
			   
	
															
	
					  
												  
	
									  
	
									 
							
								   
																 
														 
	 
					   
											
													 
										  
		   
										  
										 
															  
							   
																						 
																	   
														   
									
																   
					
			 
										   
															  
									   
					  
	
				 
  
														   
						 
								
								   
																							   
	  
								
							 
																	  
	  
																
															  
	
											
  
								  
					
			
	
								   
	
																									
	
																											  
							  
	
									
																							 
													  
																					 
											  
				
	  
								  
	  
																	   
											   
																   
														   
	
					 
	
	
									   
																					 
													  
																						
												 
				
	  
								  
	  
																	   
												  
																   
														   
	
																															  
													
					  
  
							  
					
																															  
													  
			
	
									   
	
								
								   
																		  
																							
																												
																		   
																
									
	  
														
																					   
															  
				  
		
											
		
																		 
												 
														  
											
				 
																	   
																					
	  
						   
	
						   
										  
																											  
																		 
													  
									  
	  
																	   
																 
																				
	
						   
	
							
									  
																		 
					   
	
						   
	
										  
								 
																				 
																			   
	
						   
	
							
							  
									
										
																			  
															 
									   
						   
													   
		   
														   
															 
															 
																   
	
																													   
												 
						  
  def write_error_log(self, error_message):
    if self.no_logs:
      return
    
    error_log_str = self.get_log_header()
    
    error_log_str += error_message
    
    error_log_output_path = os.path.join(self.randomized_output_folder, "WW Random %s - Error Log.txt" % self.seed)
    with open(error_log_output_path, "w") as f:
      f.write(error_log_str)
  
  def disassemble_all_code(self):
    disassemble.disassemble_all_code(self)
							  