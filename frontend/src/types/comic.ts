export interface DialogueItem {
  speaker: string;
  text: string;
  emotion?: string;
  bubble_type?: 'speech' | 'thought' | 'shout' | 'whisper';
}

export interface Panel {
  id: string;
  project_id: string;
  panel_number: number;
  title?: string;
  scene_description?: string;
  narration?: string;
  dialogue?: DialogueItem[];
  speaker?: string;
  sound_effect?: string;
  image_prompt?: string;
  image_path?: string;
  status: 'pending' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
}

export interface Character {
  id: string;
  project_id: string;
  name: string;
  description?: string;
  appearance?: string;
  personality?: string;
  clothing?: string;
  colors?: string;
  reference_image_path?: string;
}

export interface Project {
  id: string;
  title: string;
  original_prompt: string;
  character_name: string;
  setting: string;
  tone: string;
  art_style: string;
  panel_count: number;
  status: 'draft' | 'generating' | 'completed' | 'failed';
  error_message?: string;
  created_at: string;
  updated_at: string;
  characters: Character[];
  panels: Panel[];
}

export interface CreateProjectPayload {
  original_prompt: string;
  character_name: string;
  setting: string;
  tone: string;
  art_style: string;
  panel_count: string;
}

export interface GenerationStatus {
  project_id: string;
  status: string;
  error_message?: string;
  completed_panels: number;
  total_panels: number;
  progress_percentage: number;
}
