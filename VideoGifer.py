import os
import subprocess
import random
import tempfile
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

class VideoGiferApp:
    def __init__(self, root):
        self.root = root
        root.title("VideoGifer v1.0 Build")
        root.geometry("800x700")
        root.minsize(700, 650)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 24, 'bold'), foreground='#333333')
        self.style.configure('Subheader.TLabel', font=('Segoe UI', 10), foreground='#666666')
        self.style.configure('TButton', font=('Segoe UI', 9), padding=5)
        self.style.configure('TEntry', padding=5)
        self.style.configure('TCheckbutton', background='#f0f0f0')
        self.style.configure('TRadiobutton', background='#f0f0f0')
        
        # Main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Parameters
        self.parameters = {
            'ffmpeg_path': '',
            'gif_dir': '',
            'audio_file': '',
            'final_video': '',
            'loop_duration': 30,
            'num_gifs_in_loop': 5,
            'use_all_gifs': True,
            'speed_factor': 1.0,
            'zoom_effects': True,
            'zoom_intensity': 1.5,
            'output_resolution': '1920x1080',
            'bpm': 120
        }

        # Create GUI elements
        self.create_widgets()
        
        # Configure grid weights for resizing
        self.main_frame.columnconfigure(1, weight=1)
        for i in range(18):
            self.main_frame.rowconfigure(i, weight=0)
        self.main_frame.rowconfigure(15, weight=1)  # Extra space before buttons

    def create_widgets(self):
        # Header
        ttk.Label(self.main_frame, text="VideoGifer", style='Header.TLabel').grid(row=0, column=0, columnspan=3, pady=(0, 5))
        ttk.Label(self.main_frame, text="v1.0 Build", style='Subheader.TLabel').grid(row=1, column=0, columnspan=3, pady=(0, 15), sticky='w')

        # Create a frame for input fields
        input_frame = ttk.Frame(self.main_frame)
        input_frame.grid(row=2, column=0, columnspan=3, sticky='nsew', pady=(0, 10))
        
        # Configure input frame grid
        for i in range(14):
            input_frame.rowconfigure(i, pad=5)
        input_frame.columnconfigure(1, weight=1)

        # FFmpeg Path
        row = 0
        ttk.Label(input_frame, text="FFmpeg Path:").grid(row=row, column=0, padx=5, sticky='e')
        self.ffmpeg_path_entry = ttk.Entry(input_frame, width=50)
        self.ffmpeg_path_entry.grid(row=row, column=1, padx=5, sticky='ew')
        self.ffmpeg_path_entry.insert(0, "Select your FFmpeg executable...")
        self.ffmpeg_path_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.ffmpeg_path_entry, "Select your FFmpeg executable..."))
        self.ffmpeg_path_entry.bind("<FocusOut>", lambda e: self.add_placeholder(self.ffmpeg_path_entry, "Select your FFmpeg executable..."))
        ttk.Button(input_frame, text="Browse...", command=self.browse_ffmpeg_path).grid(row=row, column=2, padx=5)

        # GIF Directory
        row += 1
        ttk.Label(input_frame, text="GIF Directory:").grid(row=row, column=0, padx=5, sticky='e')
        self.gif_dir_entry = ttk.Entry(input_frame, width=50)
        self.gif_dir_entry.grid(row=row, column=1, padx=5, sticky='ew')
        self.gif_dir_entry.insert(0, "Select your GIF directory...")
        self.gif_dir_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.gif_dir_entry, "Select your GIF directory..."))
        self.gif_dir_entry.bind("<FocusOut>", lambda e: self.add_placeholder(self.gif_dir_entry, "Select your GIF directory..."))
        ttk.Button(input_frame, text="Browse...", command=self.browse_gif_dir).grid(row=row, column=2, padx=5)

        # Audio File
        row += 1
        ttk.Label(input_frame, text="Audio File:").grid(row=row, column=0, padx=5, sticky='e')
        self.audio_file_entry = ttk.Entry(input_frame, width=50)
        self.audio_file_entry.grid(row=row, column=1, padx=5, sticky='ew')
        self.audio_file_entry.insert(0, "Select your audio file...")
        self.audio_file_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.audio_file_entry, "Select your audio file..."))
        self.audio_file_entry.bind("<FocusOut>", lambda e: self.add_placeholder(self.audio_file_entry, "Select your audio file..."))
        ttk.Button(input_frame, text="Browse...", command=self.browse_audio_file).grid(row=row, column=2, padx=5)

        # Final Video Path
        row += 1
        ttk.Label(input_frame, text="Final Video Path:").grid(row=row, column=0, padx=5, sticky='e')
        self.final_video_entry = ttk.Entry(input_frame, width=50)
        self.final_video_entry.grid(row=row, column=1, padx=5, sticky='ew')
        self.final_video_entry.insert(0, "Select where to save final video...")
        self.final_video_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.final_video_entry, "Select where to save final video..."))
        self.final_video_entry.bind("<FocusOut>", lambda e: self.add_placeholder(self.final_video_entry, "Select where to save final video..."))
        ttk.Button(input_frame, text="Browse...", command=self.browse_final_video).grid(row=row, column=2, padx=5)

        # Loop Duration
        row += 1
        ttk.Label(input_frame, text="Loop Duration (s):").grid(row=row, column=0, padx=5, sticky='e')
        self.loop_duration_entry = ttk.Entry(input_frame, width=20)
        self.loop_duration_entry.grid(row=row, column=1, padx=5, sticky='w')
        self.loop_duration_entry.insert(0, str(self.parameters['loop_duration']))

        # Number of GIFs
        row += 1
        ttk.Label(input_frame, text="Number of GIFs:").grid(row=row, column=0, padx=5, sticky='e')
        self.num_gifs_entry = ttk.Entry(input_frame, width=20)
        self.num_gifs_entry.grid(row=row, column=1, padx=5, sticky='w')
        self.num_gifs_entry.insert(0, str(self.parameters['num_gifs_in_loop']))

        # Speed Factor
        row += 1
        ttk.Label(input_frame, text="Speed Factor:").grid(row=row, column=0, padx=5, sticky='e')
        self.speed_factor_entry = ttk.Entry(input_frame, width=20)
        self.speed_factor_entry.grid(row=row, column=1, padx=5, sticky='w')
        self.speed_factor_entry.insert(0, str(self.parameters['speed_factor']))

        # Zoom Intensity
        row += 1
        ttk.Label(input_frame, text="Zoom Intensity:").grid(row=row, column=0, padx=5, sticky='e')
        self.zoom_intensity_entry = ttk.Entry(input_frame, width=20)
        self.zoom_intensity_entry.grid(row=row, column=1, padx=5, sticky='w')
        self.zoom_intensity_entry.insert(0, str(self.parameters['zoom_intensity']))

        # Resolution
        row += 1
        ttk.Label(input_frame, text="Resolution:").grid(row=row, column=0, padx=5, sticky='e')
        resolution_frame = ttk.Frame(input_frame)
        resolution_frame.grid(row=row, column=1, padx=5, sticky='w')
        self.resolution_var = tk.StringVar(value='1920x1080')
        ttk.Radiobutton(resolution_frame, text='1920x1080', variable=self.resolution_var, value='1920x1080').pack(side='left')
        ttk.Radiobutton(resolution_frame, text='1080x1080', variable=self.resolution_var, value='1080x1080').pack(side='left', padx=10)
        ttk.Radiobutton(resolution_frame, text='1080x1920', variable=self.resolution_var, value='1080x1920').pack(side='left')

        # Use All GIFs
        row += 1
        self.use_all_gifs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Use All GIFs", variable=self.use_all_gifs_var).grid(row=row, column=1, padx=5, sticky='w')

        # Apply Zoom Effects
        row += 1
        self.zoom_effects_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Apply Zoom Effects", variable=self.zoom_effects_var).grid(row=row, column=1, padx=5, sticky='w')

        # BPM Sync
        row += 1
        ttk.Label(input_frame, text="BPM:").grid(row=row, column=0, padx=5, sticky='e')
        self.bpm_entry = ttk.Entry(input_frame, width=20)
        self.bpm_entry.grid(row=row, column=1, padx=5, sticky='w')
        self.bpm_entry.insert(0, str(self.parameters['bpm']))

        # Progress Bar
        row += 1
        ttk.Label(input_frame, text="Progress:").grid(row=row, column=0, padx=5, sticky='e')
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(input_frame, variable=self.progress_var, maximum=100, length=300)
        self.progress_bar.grid(row=row, column=1, padx=5, sticky='ew')
        self.progress_label = ttk.Label(input_frame, text="0%")
        self.progress_label.grid(row=row, column=2, padx=5)

        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=16, column=0, columnspan=3, pady=(20, 10), sticky='ew')
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # Generate Button
        self.process_button = tk.Button(button_frame, text="Generate", command=self.process_videos, 
                                     bg='#4CAF50', fg='white', font=("Segoe UI", 12, "bold"),
                                     padx=20, pady=5, bd=0, highlightthickness=0)
        self.process_button.grid(row=0, column=1, pady=5, sticky='nsew')

        # Footer
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.grid(row=17, column=0, columnspan=3, sticky='ew', pady=(10, 0))
        
        ttk.Label(footer_frame, text="Developed by Luma", font=("Segoe UI", 8)).pack(side='left', padx=5)
        
        # Help button with better styling
        help_button = tk.Button(footer_frame, text="Help me to buy food? Hungryy rahhh---", 
                              command=lambda: webbrowser.open("https://ko-fi.com/lumacodes"),
                              fg='white', bg='#FF5722', font=("Segoe UI", 8, "bold"),
                              bd=0, padx=10, pady=3, highlightthickness=0)
        help_button.pack(side='right', padx=5)

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def add_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(foreground='grey')

    def browse_ffmpeg_path(self):
        path = filedialog.askopenfilename()
        if path:
            self.ffmpeg_path_entry.delete(0, tk.END)
            self.ffmpeg_path_entry.insert(0, path)

    def browse_gif_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.gif_dir_entry.delete(0, tk.END)
            self.gif_dir_entry.insert(0, directory)

    def browse_audio_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.audio_file_entry.delete(0, tk.END)
            self.audio_file_entry.insert(0, path)

    def browse_final_video(self):
        path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if path:
            self.final_video_entry.delete(0, tk.END)
            self.final_video_entry.insert(0, path)

    def process_videos(self):
        # Update parameters from GUI inputs
        self.parameters['ffmpeg_path'] = self.ffmpeg_path_entry.get()
        self.parameters['gif_dir'] = self.gif_dir_entry.get()
        self.parameters['audio_file'] = self.audio_file_entry.get()
        self.parameters['final_video'] = self.final_video_entry.get()
        self.parameters['loop_duration'] = int(self.loop_duration_entry.get()) if self.loop_duration_entry.get() else self.parameters['loop_duration']
        self.parameters['num_gifs_in_loop'] = int(self.num_gifs_entry.get()) if self.num_gifs_entry.get() else self.parameters['num_gifs_in_loop']
        self.parameters['speed_factor'] = float(self.speed_factor_entry.get()) if self.speed_factor_entry.get() else self.parameters['speed_factor']
        self.parameters['zoom_intensity'] = float(self.zoom_intensity_entry.get()) if self.zoom_intensity_entry.get() else self.parameters['zoom_intensity']
        self.parameters['output_resolution'] = self.resolution_var.get()
        self.parameters['use_all_gifs'] = self.use_all_gifs_var.get()
        self.parameters['zoom_effects'] = self.zoom_effects_var.get()
        self.parameters['bpm'] = int(self.bpm_entry.get()) if self.bpm_entry.get() else self.parameters['bpm']

        # Handle speed factor and zoom intensity zero values
        if self.parameters['speed_factor'] <= 0:
            self.parameters['speed_factor'] = 0.1
        if self.parameters['zoom_intensity'] <= 0:
            self.parameters['zoom_intensity'] = 0.1

        # Add buffer to loop duration
        buffer_duration = 4 if self.parameters['loop_duration'] <= 30 else 8
        adjusted_loop_duration = self.parameters['loop_duration'] + buffer_duration
        self.parameters['loop_duration'] = adjusted_loop_duration

        # Start video processing
        self.root.after(100, self.create_video)  # Run the video processing after a short delay

    def create_video(self):
        # Extract parameters
        ffmpeg_path = self.parameters['ffmpeg_path']
        gif_dir = self.parameters['gif_dir']
        audio_file = self.parameters['audio_file']
        final_video = self.parameters['final_video']
        loop_duration = self.parameters['loop_duration']
        num_gifs_in_loop = self.parameters['num_gifs_in_loop']
        speed_factor = self.parameters['speed_factor']
        zoom_effects = self.parameters['zoom_effects']
        zoom_intensity = self.parameters['zoom_intensity']
        output_resolution = self.parameters['output_resolution']
        use_all_gifs = self.parameters['use_all_gifs']
        bpm = self.parameters['bpm']

        # Validate inputs
        if not (ffmpeg_path and gif_dir and audio_file and final_video):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # Calculate GIF display duration based on BPM
        beat_duration = 60 / bpm
        gif_duration = beat_duration * speed_factor

        # Gather GIFs
        gif_files = [os.path.join(gif_dir, f) for f in os.listdir(gif_dir) if f.lower().endswith('.gif')]
        if not gif_files:
            messagebox.showerror("Error", "No GIF files found in the selected directory.")
            return

        # Create temporary directory for intermediate video files
        temp_dir = tempfile.mkdtemp()

        try:
            video_parts = []
            total_duration = 0

            while total_duration < loop_duration:
                random.shuffle(gif_files)  # Shuffle to distribute GIFs randomly
                for gif_file in gif_files:
                    if total_duration >= loop_duration:
                        break

                    # Convert GIF to video with desired duration
                    video_part = os.path.join(temp_dir, f'part_{len(video_parts)}.mp4')
                    self.convert_gif_to_video(ffmpeg_path, gif_file, video_part, gif_duration, zoom_effects, zoom_intensity, output_resolution)
                    video_parts.append(video_part)
                    total_duration += gif_duration

            # If the total duration exceeds the loop duration, trim the last part
            if total_duration > loop_duration:
                last_part_duration = gif_duration - (total_duration - loop_duration)
                self.trim_video(ffmpeg_path, video_parts[-1], last_part_duration)

            # Concatenate videos
            concatenated_video = os.path.join(temp_dir, 'concatenated.mp4')
            self.concatenate_videos(ffmpeg_path, video_parts, concatenated_video)

            # Add audio to video
            self.add_audio_to_video(ffmpeg_path, concatenated_video, audio_file, final_video)

            # Final progress update
            self.update_progress(100)
            messagebox.showinfo("Success", "Video processing complete!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Clean up temporary files
            shutil.rmtree(temp_dir)

    def convert_gif_to_video(self, ffmpeg_path, gif_file, output_file, duration, zoom_effects, zoom_intensity, resolution):
        filter_complex = ""
        if zoom_effects:
            filter_complex = f"zoompan=z='min(max(zoom,pzoom)+0.0015*{zoom_intensity},1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',"
        command = [
            ffmpeg_path, '-y', '-i', gif_file,
            '-vf', f"{filter_complex}scale={resolution},setsar=1",
            '-t', str(duration),
            '-r', '30',
            '-pix_fmt', 'yuv420p',
            output_file
        ]
        subprocess.run(command, check=True)
        self.update_progress(self.progress_var.get() + (100 / len(os.listdir(self.parameters['gif_dir']))))

    def trim_video(self, ffmpeg_path, video_file, duration):
        temp_file = video_file + "_trimmed.mp4"
        command = [
            ffmpeg_path, '-y', '-i', video_file,
            '-t', str(duration),
            '-c', 'copy',
            temp_file
        ]
        subprocess.run(command, check=True)
        os.remove(video_file)
        os.rename(temp_file, video_file)

    def concatenate_videos(self, ffmpeg_path, video_files, output_file):
        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            for video_file in video_files:
                f.write(f"file '{video_file}'\n")
            concat_file = f.name
        command = [
            ffmpeg_path, '-y', '-f', 'concat', '-safe', '0', '-i', concat_file,
            '-c', 'copy', output_file
        ]
        subprocess.run(command, check=True)
        os.remove(concat_file)

    def add_audio_to_video(self, ffmpeg_path, video_file, audio_file, output_file):
        command = [
            ffmpeg_path, '-y', '-i', video_file, '-i', audio_file,
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
            '-shortest', output_file
        ]
        subprocess.run(command, check=True)

    def update_progress(self, progress):
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{int(progress)}%")
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGiferApp(root)
    root.mainloop()