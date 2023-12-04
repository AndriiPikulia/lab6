import os
import subprocess
from typing import List

subprocess.run(["pip", "install", "spotipy"])

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyPlaylistManager:
    def __init__(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id='9ea25ee321bf4655804dc2cea25c2c43',
            client_secret='2fea13c3944c4fa2a022234b161ee438'
        ))
        self.current_playlist = None

    def search(self, query: str) -> None:
        results = self.sp.search(query)
        tracks = results['tracks']['items']
        for i, track in enumerate(tracks, start=1):
            print(f"{i}. {track['name']} - {track['artists'][0]['name']}")

    def add_track(self, track_index: int, query: str) -> None:
        if self.current_playlist:
            results = self.sp.search(query)
            tracks = results['tracks']['items']
            if 1 <= track_index <= len(tracks):
                track = tracks[track_index - 1]
                with open(self.current_playlist.filename, 'a') as file:
                    file.write(f"{track['name']} - {track['artists'][0]['name']}\n")
                print("Трек додано до плейліста.")
            else:
                print("Невірний номер трека.")
        else:
            print("Немає активного плейліста для додавання трека.")

    def remove_track(self, track_index: int) -> None:
        if self.current_playlist:
            with open(self.current_playlist.filename, 'r') as file:
                lines = file.readlines()
            if 1 <= track_index <= len(lines):
                removed_track = lines.pop(track_index - 1)
                with open(self.current_playlist.filename, 'w') as file:
                    file.writelines(lines)
                print(f"Трек {track_index}. {removed_track.strip()} видалено з плейліста.")
            else:
                print("Невірний номер трека.")
        else:
            print("Немає активного плейліста для видалення трека.")

    def create_playlist(self, playlist_name: str) -> 'Playlist':
        playlist = Playlist(playlist_name, self.current_directory)
        print(f"Створено новий плейліст '{playlist_name}'.")
        return playlist

    def switch_playlist(self) -> None:
        playlists = self.get_available_playlists()
        if not playlists:
            print("Немає доступних плейлістів.")
            return

        print("Доступні плейлісти:")
        for i, playlist in enumerate(playlists, start=1):
            print(f"{i}. {playlist}")
        try:
            playlist_index = int(input("Виберіть номер плейліста для перемикання (або 0, щоб повернутися): "))
            if 0 < playlist_index <= len(playlists):
                playlist_name = playlists[playlist_index - 1]
                self.current_playlist = Playlist(playlist_name, self.current_directory)
                print(f"Перемкнуто на плейліст '{playlist_name}'.")
            elif playlist_index == 0:
                pass
            else:
                print("Невірний номер плейліста.")
        except ValueError:
            print("Будь ласка, введіть коректний номер плейліста.")

    def delete_playlist(self) -> None:
        if self.current_playlist:
            playlist_name = self.current_playlist.name
            playlist_filename = os.path.join(self.current_directory, f'{playlist_name}.txt')
            if os.path.exists(playlist_filename):
                os.remove(playlist_filename)
                print(f"Плейлист '{playlist_name}' видалено.")
                self.current_playlist = None
            else:
                print(f"Помилка: файл плейліста '{playlist_name}.txt' не знайдено.")
        else:
            print("Немає активного плейліста для видалення.")

    def get_available_playlists(self) -> List[str]:
        playlists = [f.replace('.txt', '') for f in os.listdir(self.current_directory) if f.endswith('.txt')]
        return playlists

    def display_tracks(self) -> None:
        if self.current_playlist:
            self.current_playlist.display_tracks()
        else:
            print("Немає активного плейліста для виведення.")

class Playlist:
    def __init__(self, name: str, directory: str):
        self.name = name
        self.filename = os.path.join(directory, f'{name}.txt')
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.playlist_content = file.readlines()
        else:
            self.playlist_content = []
            with open(self.filename, 'w') as file:
                file.write(f"Плейліст '{name}':\n")

    def display_tracks(self) -> None:
        for i, track in enumerate(self.playlist_content, start=0):
            print(f"{i}. {track.strip()}")

def main() -> None:
    playlist_manager = SpotifyPlaylistManager()
    while True:
        print("\n1. Пошук трека")
        print("2. Вивести плейліст")
        print("3. Видалити трек з плейліста")
        print("4. Створити новий плейліст")
        print("5. Перемкнутися на інший плейліст")
        print("6. Видалити плейліст")
        print("7. Вийти")
        choice = input("Оберіть опцію: ")

        if choice == '1':
            query = input("Введіть назву трека або виконавця: ")
            playlist_manager.search(query)
            try:
                track_index = int(input("Виберіть номер трека для додавання до плейліста (або 0, щоб повернутися): "))
                if track_index != 0:
                    playlist_manager.add_track(track_index, query)
            except ValueError:
                print("Будь ласка, введіть коректний номер трека.")
        elif choice == '2':
            playlist_manager.display_tracks()
        elif choice == '3':
            if playlist_manager.current_playlist:
                playlist_manager.current_playlist.display_tracks()
                try:
                    track_index = int(input("Виберіть номер трека для видалення з плейліста (або 0, щоб повернутися): "))
                    if track_index != 0:
                        playlist_manager.remove_track(track_index)
                except ValueError:
                    print("Будь ласка, введіть коректний номер трека.")
            else:
                print("Немає активного плейліста для видалення трека.")
        elif choice == '4':
            playlist_name = input("Введіть назву нового плейліста: ")
            playlist_manager.current_playlist = playlist_manager.create_playlist(playlist_name)
        elif choice == '5':
            playlist_manager.switch_playlist()
        elif choice == '6':
            playlist_manager.delete_playlist()
        elif choice == '7':
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()