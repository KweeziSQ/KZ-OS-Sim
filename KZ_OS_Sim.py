import copy
import datetime
import hashlib
import sys
import io
import os
import pickle
import re
import time
import random
import json
import tkinter as tk
import traceback
from tkinter import ttk, messagebox, simpledialog, scrolledtext, colorchooser, filedialog
from PIL import Image, ImageTk


def resource_path(relative_path):
    """ Возвращает абсолютный путь к ресурсу, работает для IDE и для PyInstaller """
    try:
        # PyInstaller создает временную папку в sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Если запускается не из PyInstaller, base_path - это директория скрипта
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Словарь для переводов
translations = {
    "RU": {
        # Общие
        "error": "Ошибка",
        "warning": "Предупреждение",
        "info": "Информация",
        "ok": "OK",
        "cancel": "Отмена",
        "yes": "Да",
        "no": "Нет",
        "exit_prompt_title": "Выход",
        "exit_prompt_message": "Сохранить состояние перед выходом?",
        "save_state_menu": "Сохранить состояние",
        "exit_menu": "Выход",
        "file_menu": "Файл",
        "apps_menu": "Приложения",
        # LoginWindow
        "login_title": "Вход в SimOS",
        "username_label": "Имя пользователя:",
        "password_label": "Пароль:",
        "login_button": "Войти",
        "login_err_user_not_found": "Пользователь '{username}' не найден.",
        "login_err_wrong_password": "Неверный пароль.",
        # DesktopWindow
        "desktop_title": "{os_name} - Рабочий стол [{user}]",
        "explorer_app": "Проводник",
        "calculator_app": "Калькулятор",
        "terminal_app": "Терминал",
        "start_button": "Пуск",
        "start_menu_exit": "Выход", # Повтор для меню Пуск
        # FileExplorerWindow
        "explorer_title": "Проводник SimOS",
        "up_button": "↑ Вверх",
        "path_label": "Путь:",
        "refresh_button": "Обн.",
        "folder_button": "Папка",
        "file_button": "Файл",
        "delete_button": "Удалить",
        "rename_button": "Переим.",
        "properties_button": "Свойства",
        "tree_col_name": "Имя",
        "tree_col_type": "Тип",
        "tree_col_size": "Размер",
        "tree_col_owner": "Владелец",
        "tree_col_permissions": "Права",
        "new_folder_title": "Создать папку",
        "new_folder_prompt": "Введите имя новой папки:",
        "new_file_title": "Создать файл",
        "new_file_prompt": "Введите имя нового файла:",
        "rename_title": "Переименовать",
        "rename_prompt": "Введите новое имя для '{old_name}':",
        "delete_title": "Подтверждение удаления",
        "delete_prompt": "Удалить:\n{items}\n(Папки удаляются рекурсивно!)",
        "delete_warn_select": "Не выбран элемент.",
        "delete_warn_multi": "Пожалуйста, выберите только один элемент.",
        "delete_info_success": "Успешно удалено: {count} элемент(ов).",
        "delete_warn_errors": "Удаление завершено с ошибками. Успешно: {success}. Ошибок: {errors}.",
        "properties_title": "Свойства: {name}",
        "properties_name": "Имя:",
        "properties_type": "Тип:",
        "properties_size": "Размер:",
        "properties_size_bytes": "{size} байт",
        "properties_path": "Путь:",
        "properties_owner": "Владелец:",
        "properties_permissions": "Права:",
        "properties_mtime": "Изм.:",
        "file_content_title": "Содержимое: {filename}",
        "error_nav": "Ошибка навигации",
        "error_read_dir": "Ошибка при чтении каталога",
        "error_read_file": "Ошибка чтения файла",
        "error_create_folder": "Ошибка создания папки",
        "error_create_file": "Ошибка создания файла",
        "error_delete": "Ошибка удаления",
        "error_rename": "Ошибка переименования",
        "error_props": "Ошибка свойств",
        "error_props_get": "Не удалось получить свойства",
        "error_sort_get": "Не удалось получить данные для сортировки колонки '{col}'.",
        "error_sort_title": "Ошибка сортировки",
        "warn_invalid_name": "Неверное имя",
        "warn_invalid_name_folder": "Имя папки не должно содержать / или \\",
        "warn_invalid_name_file": "Имя файла не должно содержать / или \\",
        # CalculatorWindow
        "calculator_title": "Калькулятор",
        "calc_err_div_zero": "Ошибка: /0",
        "calc_err_generic": "Ошибка",
        # TerminalWindow
        "terminal_title": "Терминал - {user}",
        # ... добавьте другие ключи по мере необходимости
        "settings_app": "Настройки",
        "settings_title": "Настройки SimOS",
        "os_info_label": "Информация о системе:",
        "os_version_label": "Версия ОС:",
        "desktop_bg_label": "Фон рабочего стола:",
        "choose_color_button": "Выбрать цвет...",
        "choose_bg_color": "Выберите цвет фона",  # Заголовок для colorchooser

        "taskmgr_app": "Диспетчер задач",
        "taskmgr_title": "Диспетчер задач SimOS",
        "taskmgr_cpu_label": "ЦП ({cores} ядра):",
        "taskmgr_ram_label": "Память:",
        "taskmgr_ram_usage": "{used:.1f} МБ / {total:.1f} МБ",
        "taskmgr_processes_label": "Процессы:",
        "taskmgr_kill_button": "Снять задачу",
        "taskmgr_pid_col": "PID",
        "taskmgr_user_col": "Пользователь",
        "taskmgr_cpu_col": "ЦП (%)",
        "taskmgr_ram_col": "Память (МБ)",
        "taskmgr_command_col": "Команда",
        "taskmgr_kill_confirm_title": "Подтверждение",
        "taskmgr_kill_confirm_msg": "Завершить процесс {pid} ({command})?",
        "taskmgr_kill_error_title": "Ошибка завершения",
        "taskmgr_kill_error_noperm": "Отказано в доступе: Нельзя завершить этот процесс.",
        "taskmgr_kill_error_noexist": "Процесс с PID {pid} не найден.",
        "taskmgr_kill_error_kernel": "Нельзя завершить системный процесс (PID 1).",

        "appearance_label": "Внешний вид",
        "wallpaper_label": "Обои рабочего стола:",
        "browse_button": "Обзор...",
        "select_wallpaper_title": "Выберите файл обоев",

        "editor_app": "Редактор",
        "editor_title": "Текстовый редактор",
        "editor_menu_file": "Файл",
        "editor_menu_new": "Новый",
        "editor_menu_open": "Открыть...",
        "editor_menu_save": "Сохранить",
        "editor_menu_save_as": "Сохранить как...",
        "editor_menu_exit": "Выход",
        "editor_open_title": "Открыть файл",
        "editor_save_title": "Сохранить файл как",
        "editor_save_confirm_title": "Сохранить изменения",
        "editor_save_confirm_msg": "Сохранить изменения в файле '{filename}' перед закрытием?",
        "editor_untitled": "Безымянный",
        "start_menu_apps": "Приложения",
        "start_menu_system": "Система",
        "taskbar_pin": "Закрепить на панели задач",
        "taskbar_unpin": "Открепить от панели задач",
        "taskbar_activate": "Активировать",
        "taskbar_close": "Закрыть окно",

        "snake_app": "Змейка",
        "snake_title": "Игра Змейка",
        "snake_score": "Счет: {score}",
        "snake_game_over": "ИГРА ОКОНЧЕНА!",
    },
    "EN": {
        # General
        "error": "Error",
        "warning": "Warning",
        "info": "Information",
        "ok": "OK",
        "cancel": "Cancel",
        "yes": "Yes",
        "no": "No",
        "exit_prompt_title": "Exit",
        "exit_prompt_message": "Save state before exiting?",
        "save_state_menu": "Save State",
        "exit_menu": "Exit",
        "file_menu": "File",
        "apps_menu": "Applications",
        # LoginWindow
        "login_title": "SimOS Login",
        "username_label": "Username:",
        "password_label": "Password:",
        "login_button": "Login",
        "login_err_user_not_found": "User '{username}' not found.",
        "login_err_wrong_password": "Incorrect password.",
        # DesktopWindow
        "desktop_title": "{os_name} - Desktop [{user}]",
        "explorer_app": "Explorer",
        "calculator_app": "Calculator",
        "terminal_app": "Terminal",
        "start_button": "Start",
        "start_menu_exit": "Exit",
        # FileExplorerWindow
        "explorer_title": "SimOS Explorer",
        "up_button": "↑ Up",
        "path_label": "Path:",
        "refresh_button": "Refresh",
        "folder_button": "Folder",
        "file_button": "File",
        "delete_button": "Delete",
        "rename_button": "Rename",
        "properties_button": "Properties",
        "tree_col_name": "Name",
        "tree_col_type": "Type",
        "tree_col_size": "Size",
        "tree_col_owner": "Owner",
        "tree_col_permissions": "Permissions",
        "new_folder_title": "Create Folder",
        "new_folder_prompt": "Enter new folder name:",
        "new_file_title": "Create File",
        "new_file_prompt": "Enter new file name:",
        "rename_title": "Rename",
        "rename_prompt": "Enter new name for '{old_name}':",
        "delete_title": "Confirm Deletion",
        "delete_prompt": "Delete:\n{items}\n(Folders are deleted recursively!)",
        "delete_warn_select": "No item selected.",
        "delete_warn_multi": "Please select only one item.",
        "delete_info_success": "Successfully deleted: {count} item(s).",
        "delete_warn_errors": "Deletion finished with errors. Success: {success}. Errors: {errors}.",
        "properties_title": "Properties: {name}",
        "properties_name": "Name:",
        "properties_type": "Type:",
        "properties_size": "Size:",
        "properties_size_bytes": "{size} bytes",
        "properties_path": "Path:",
        "properties_owner": "Owner:",
        "properties_permissions": "Permissions:",
        "properties_mtime": "Modified:",
        "file_content_title": "Content: {filename}",
        "error_nav": "Navigation Error",
        "error_read_dir": "Error reading directory",
        "error_read_file": "Error reading file",
        "error_create_folder": "Error creating folder",
        "error_create_file": "Error creating file",
        "error_delete": "Error deleting item",
        "error_rename": "Error renaming item",
        "error_props": "Properties Error",
        "error_props_get": "Failed to get properties",
        "error_sort_get": "Failed to get data for sorting column '{col}'.",
        "error_sort_title": "Sort Error",
        "warn_invalid_name": "Invalid Name",
        "warn_invalid_name_folder": "Folder name cannot contain / or \\",
        "warn_invalid_name_file": "File name cannot contain / or \\",
         # CalculatorWindow
        "calculator_title": "Calculator",
        "calc_err_div_zero": "Error: Div by zero",
        "calc_err_generic": "Error",
        # TerminalWindow
        "terminal_title": "Terminal - {user}",
        # В translations["EN"]
        "settings_app": "Settings",
        "settings_title": "SimOS Settings",
        "os_info_label": "System Information:",
        "os_version_label": "OS Version:",
        "desktop_bg_label": "Desktop Background:",
        "choose_color_button": "Choose Color...",
        "choose_bg_color": "Select Background Color",

        # В translations["EN"]
        "taskmgr_app": "Task Manager",
        "taskmgr_title": "SimOS Task Manager",
        "taskmgr_cpu_label": "CPU ({cores} cores):",
        "taskmgr_ram_label": "Memory:",
        "taskmgr_ram_usage": "{used:.1f} MB / {total:.1f} MB",
        "taskmgr_processes_label": "Processes:",
        "taskmgr_kill_button": "End Task",
        "taskmgr_pid_col": "PID",
        "taskmgr_user_col": "User",
        "taskmgr_cpu_col": "CPU (%)",
        "taskmgr_ram_col": "Memory (MB)",
        "taskmgr_command_col": "Command",
        "taskmgr_kill_confirm_title": "Confirm",
        "taskmgr_kill_confirm_msg": "End process {pid} ({command})?",
        "taskmgr_kill_error_title": "Termination Error",
        "taskmgr_kill_error_noperm": "Permission denied: Cannot terminate this process.",
        "taskmgr_kill_error_noexist": "Process with PID {pid} not found.",
        "taskmgr_kill_error_kernel": "Cannot terminate system process (PID 1).",

        "appearance_label": "Appearance",
        "wallpaper_label": "Desktop Wallpaper:",
        "browse_button": "Browse...",
        "select_wallpaper_title": "Select Wallpaper File",

        "editor_app": "Editor",
        "editor_title": "Text Editor",
        "editor_menu_file": "File",
        "editor_menu_new": "New",
        "editor_menu_open": "Open...",
        "editor_menu_save": "Save",
        "editor_menu_save_as": "Save As...",
        "editor_menu_exit": "Exit",
        "editor_open_title": "Open File",
        "editor_save_title": "Save File As",
        "editor_save_confirm_title": "Save Changes",
        "editor_save_confirm_msg": "Save changes to file '{filename}' before closing?",
        "editor_untitled": "Untitled",
        "start_menu_apps": "Applications",
        "start_menu_system": "System",
        "taskbar_pin": "Pin to taskbar",
        "taskbar_unpin": "Unpin from taskbar",
        "taskbar_activate": "Activate",
        "taskbar_close": "Close window",

        "snake_app": "Snake",
        "snake_title": "Snake Game",
        "snake_score": "Score: {score}",
        "snake_game_over": "GAME OVER!",
    }
}

# Глобальная переменная для текущего языка (будет управляться из DesktopWindow)
current_language = "RU"

# Функция-переводчик
def tr(key, **kwargs):
    """Возвращает переведенную строку по ключу для текущего языка."""
    lang_dict = translations.get(current_language, translations["EN"]) # Фоллбэк на EN
    base_string = lang_dict.get(key, key) # Возвращаем ключ, если перевод не найден
    try:
        return base_string.format(**kwargs) # Форматируем строку, если переданы аргументы
    except KeyError as e:
        print(f"Предупреждение: Отсутствует аргумент '{e}' для форматирования ключа '{key}'")
        return base_string # Возвращаем неформатированную строку при ошибке


# ==============================================================================
# == КЛАСС SimulatedOS (Версия с правами, пользователями, сохранением) ==
# ==============================================================================
class SimulatedOS:
    # STATE_FILE убран отсюда, передается в __init__

    def __init__(self, state_file_path): # Добавляем аргумент state_file_path
        self.state_file = state_file_path # Сохраняем путь к файлу состояния
        # --- Состояние ОС ---
        if os.path.exists(self.state_file): # Используем self.state_file
            print(f"[SimOS] Загрузка состояния из {self.state_file}...")
            try:
                with open(self.state_file, 'rb') as f:
                    loaded_state = pickle.load(f)
                    self.__dict__.update(loaded_state.__dict__)
                print("[SimOS] Состояние успешно загружено.")
                self.current_working_directory = ['/']
                self.current_user = 'guest'
                # --- Важно: Убедимся, что нужные атрибуты есть после загрузки ---
                if not hasattr(self, 'desktop_bg_color'): self.desktop_bg_color = "#000000"
                if not hasattr(self, 'desktop_wallpaper_path'): self.desktop_wallpaper_path = "icons/default_wallpaper.png"
                if not hasattr(self, 'pinned_apps'): self.pinned_apps = ["explorer", "terminal"]
                if not hasattr(self, 'desktop_icon_positions'): self.desktop_icon_positions = {}
                if not hasattr(self, 'total_cores'): self.total_cores = 1
                if not hasattr(self, 'total_ram_mb'): self.total_ram_mb = 512
                if not hasattr(self, 'processes'): self.processes = {} # Инициализируем, если нет
                if not hasattr(self, 'next_pid'): self.next_pid = max([1] + list(self.processes.keys())) + 1 # Восстанавливаем счетчик PID
                # --- Конец проверки атрибутов ---
            except Exception as e:
                print(f"[SimOS] Ошибка загрузки состояния: {e}. Инициализация по умолчанию.")
                self._initialize_default_state()
        else:
            print("[SimOS] Файл состояния не найден. Инициализация по умолчанию.")
            self._initialize_default_state()

        self._initialize_text_commands()


    def _initialize_default_state(self):
        """Инициализирует ОС значениями по умолчанию."""
        self.os_name = "KZ OS Sim v0.1(Beta)"
        self.max_fs_size = 2896 * 2896 # 8MB
        self.desktop_bg_color = "#000000"
        self.desktop_wallpaper_path = "icons/default_wallpaper.png"
        self.total_cores = 1
        self.total_ram_mb = 512
        self.pinned_apps = ["explorer", "terminal"]
        self.desktop_icon_positions = {}

        default_guest_pass = "1234"; default_root_pass = "root"
        self.users_info = {
            'root': {'uid': 0, 'home': '/root', 'password_hash': self._hash_password(default_root_pass)},
            'guest': {'uid': 1000, 'home': '/home/guest', 'password_hash': self._hash_password(default_guest_pass)}
        }
        self.current_user = 'guest'

        now = time.time()
        default_perms_dir = 'rwxr-xr-x'; default_perms_file = 'rw-r--r--'
        self.filesystem = {
            '/': {'meta': {'owner': 'root', 'permissions': default_perms_dir, 'mtime': now, 'ctime': now, 'dir_size': 0}, 'children': {
                    'etc': {'meta': {'owner': 'root', 'permissions': default_perms_dir, 'mtime': now, 'ctime': now, 'dir_size': 0}, 'children': {
                            'passwd_file': {'meta': {'owner': 'root', 'permissions': default_perms_file, 'mtime': now, 'ctime': now}, 'content': 'root:x:0\nguest:x:1000'}
                    }},
                    'home': {'meta': {'owner': 'root', 'permissions': default_perms_dir, 'mtime': now, 'ctime': now, 'dir_size': 0}, 'children': {
                            'guest': {'meta': {'owner': 'guest', 'permissions': default_perms_dir, 'mtime': now, 'ctime': now, 'dir_size': 0}, 'children': {}}
                    }},
                    'root': {'meta': {'owner': 'root', 'permissions': 'rwx------', 'mtime': now, 'ctime': now, 'dir_size': 0}, 'children': {}},
                    'tmp': {'meta': {'owner': 'root', 'permissions': 'rwxrwxrwx', 'mtime': now, 'ctime': now, 'dir_size': 0}, 'children': {}}
            }}}
        # Пересчитаем начальные размеры папок
        self._update_directory_size('/')

        self.current_working_directory = ['/']
        self.next_pid = 1
        self.processes = {}
        self._add_process("kernel/shell", "root", cpu=random.uniform(0.5, 2.0), ram=random.uniform(50, 150))

    def _initialize_text_commands(self):
        """Инициализирует словарь текстовых команд для терминала."""
        self.text_commands = {
            'pwd': self.do_pwd_text, 'ls': self.do_ls_text, 'cd': self.do_cd_text,
            'mkdir': self.do_mkdir_text, 'touch': self.do_touch_text, 'cat': self.do_cat_text,
            'echo': self.do_echo_text, 'rm': self.do_rm_text,
            'whoami': self.do_whoami_text, 'passwd': self.do_passwd_text,
            'adduser': self.do_adduser_text, 'chmod': self.do_chmod_text,
            'help': self.do_help_text, 'clear': self.do_clear_text, 'exit': self.do_exit_text,
            # Добавьте 'ln': self.do_ln_text, если реализуете текстовую команду
        }

    def save_state(self):
        """Сохраняет текущее состояние ОС в файл."""
        print(f"[SimOS] Сохранение состояния в {self.state_file}...")
        try:
            commands_backup = self.text_commands
            self.text_commands = {}
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'wb') as f:
                pickle.dump(self, f)
            self.text_commands = commands_backup
            print("[SimOS] Состояние успешно сохранено.")
        except Exception as e:
            print(f"[SimOS] Ошибка сохранения состояния: {e}")
            traceback.print_exc()

    # --- Управление пользователями и паролями ---
    def _hash_password(self, password):
        salt = os.urandom(16); pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000); return salt + pwd_hash
    def _verify_password(self, stored_hash, provided_password):
        if not stored_hash or len(stored_hash) < 16: return False
        salt = stored_hash[:16]; stored_pwd_hash = stored_hash[16:]
        provided_pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000); return stored_pwd_hash == provided_pwd_hash
    def verify_user_password(self, username, password):
        user_info = self.users_info.get(username);
        if not user_info: return False
        stored_hash = user_info.get('password_hash'); return self._verify_password(stored_hash, password)
    def set_user_password(self, username, new_password):
        if username in self.users_info: self.users_info[username]['password_hash'] = self._hash_password(new_password); return True; return False
    def add_user(self, username, password):
        if username in self.users_info: raise ValueError(f"Пользователь '{username}' уже существует.")
        if not re.match("^[a-zA-Z0-9_-]+$", username): raise ValueError("Недопустимое имя пользователя (разрешены буквы, цифры, _, -).")
        max_uid = 1000
        for info in self.users_info.values():
            if info['uid'] >= max_uid: max_uid = info['uid'] + 1
        home_path = f"/home/{username}"
        try:
            home_parent_node, home_name, _ = self._get_parent_node_and_name(home_path)
            if home_parent_node is None or home_name is None: raise OSError("Не удалось найти родительский каталог для домашней директории.")
            if home_name in home_parent_node['children']: print(f"[adduser] Предупреждение: Домашний каталог '{home_path}' уже существует.")
            else: self.do_mkdir_internal(home_path, owner=username, permissions='rwxr-x---')
        except Exception as e: print(f"[adduser] Предупреждение: не удалось создать домашний каталог '{home_path}': {e}")
        self.users_info[username] = {'uid': max_uid, 'home': home_path, 'password_hash': self._hash_password(password)}
        print(f"[adduser] Пользователь '{username}' (UID {max_uid}) добавлен."); return True

    # --- Вспомогательные функции ФС с метаданными ---
    def _get_node_from_path(self, path_list):
        current_node = self.filesystem.get('/');
        if not current_node: return None
        if path_list == ['/']: return current_node
        for part in path_list[1:]:
            if not isinstance(current_node, dict) or 'children' not in current_node: return None
            children = current_node.get('children', {}); current_node = children.get(part)
            if current_node is None: return None
        return current_node
    def _get_parent_node_and_name(self, path_str):
        path_str = path_str.replace('\\', '/'); cleaned_path_str = path_str.rstrip('/') if path_str != '/' else '/'
        if '/' not in cleaned_path_str:
            parent_path_list = self.current_working_directory[:]; name = cleaned_path_str; parent_node = self._get_node_from_path(parent_path_list)
        elif cleaned_path_str == '/': return None, '/', None
        else:
            parent_path_str = cleaned_path_str.rsplit('/', 1)[0]; name = cleaned_path_str.rsplit('/', 1)[1]
            if not parent_path_str: parent_path_list = ['/']
            else: parent_path_list = self._resolve_path(parent_path_str)
            if parent_path_list is None: return None, None, None
            parent_node = self._get_node_from_path(parent_path_list)
        if not isinstance(parent_node, dict) or 'children' not in parent_node: return None, None, None
        if not name: return parent_node, None, parent_path_list
        return parent_node, name, parent_path_list
    def _resolve_path(self, path_str):
        if not path_str: return self.current_working_directory[:]
        path_str = path_str.replace('\\', '/')
        if path_str.startswith('/'): current_path_list = ['/']; path_components = path_str.strip('/').split('/')
        else: current_path_list = self.current_working_directory[:]; path_components = path_str.split('/')
        if not path_components or all(p == '' for p in path_components):
             if path_str.startswith('/'): return ['/']
             if not path_str or path_str == '.': return self.current_working_directory[:]
        final_path = ['/']; temp_cwd = current_path_list[:]
        if not path_str.startswith('/'): final_path = temp_cwd
        for component in path_components:
            if component == '' or component == '.': continue
            elif component == '..':
                if len(final_path) > 1: final_path.pop()
            else: final_path.append(component)
        return final_path
    def get_cwd_string(self):
        if len(self.current_working_directory) == 1 and self.current_working_directory[0] == '/': return '/'
        return '/' + '/'.join(self.current_working_directory[1:])
    def _calculate_fs_size(self, node=None): # Используется только для проверки лимита, не для отображения
        if node is None: root_node = self.filesystem.get('/'); node = root_node if root_node else {}
        size = 0
        if isinstance(node, dict):
             size += 64 # Условный размер "заголовка" папки/файла
             if 'children' in node: # Папка
                 for item in node['children'].values(): size += self._calculate_fs_size(item)
             elif 'content' in node: # Файл
                 try: size += len(node.get('content', '').encode('utf-8'))
                 except: size += len(node.get('content', ''))
        return size

    # --- Проверка прав доступа ---
    def _check_permission(self, node_meta, required_perm):
        if not node_meta or 'permissions' not in node_meta or 'owner' not in node_meta: return False
        perms = node_meta['permissions']; owner = node_meta['owner']
        if len(perms) != 9: return False
        perm_map = {'r': 0, 'w': 1, 'x': 2};
        if required_perm not in perm_map: return False
        perm_index = perm_map[required_perm]
        if self.current_user == owner: return perms[perm_index] == required_perm
        else: return perms[perm_index + 6] == required_perm # Проверка для "остальных"

    # --- Обновление размера папки ---
    def _update_directory_size(self, path_str_or_list):
        if isinstance(path_str_or_list, str): path_list = self._resolve_path(path_str_or_list)
        else: path_list = path_str_or_list
        if not path_list: return
        node = self._get_node_from_path(path_list)
        if not node or 'children' not in node:
            if len(path_list) > 1: self._update_directory_size(path_list[:-1])
            return
        current_size = 0
        for child_name, child_node in node.get('children', {}).items():
            if 'children' in child_node: current_size += child_node.get('meta', {}).get('dir_size', 0)
            elif 'content' in child_node:
                try: current_size += len(child_node.get('content', '').encode('utf-8'))
                except: current_size += len(child_node.get('content', ''))
            current_size += 64 # Размер самого узла
        if 'meta' in node: node['meta']['dir_size'] = current_size
        else: print(f"[FS Size] Warning: No meta found for {'/'.join(path_list)}")
        if len(path_list) > 1: self._update_directory_size(path_list[:-1])

    # --- Внутренние методы для создания узлов ---
    def _create_node(self, parent_node, name, node_type, owner, permissions, content=None):
        if name in parent_node['children']: raise FileExistsError(f"'{name}' уже существует.")
        now = time.time()
        new_node = {'meta': {'owner': owner, 'permissions': permissions, 'mtime': now, 'ctime': now}} # Добавлен ctime
        if node_type == 'file': new_node['content'] = content if content is not None else ""
        elif node_type == 'folder': new_node['children'] = {}; new_node['meta']['dir_size'] = 0 # Добавлен dir_size
        else: raise ValueError("Неизвестный тип узла")
        # Проверка размера диска
        estimated_size = 100 + (len(content.encode('utf-8')) if content else 0)
        current_size = self._calculate_fs_size()
        if current_size + estimated_size > self.max_fs_size: raise OSError("Недостаточно места на диске")
        parent_node['children'][name] = new_node
        parent_node['meta']['mtime'] = now
        # Обновление размера родителя будет вызвано из do_* методов
        return new_node

    # --- Модифицированные методы для GUI (с проверкой прав и обновлением размера) ---
    def do_ls_for_gui(self, path_str):
        resolved_path_list = self._resolve_path(path_str);
        if resolved_path_list is None: raise FileNotFoundError(f"Путь не найден: {path_str}")
        node = self._get_node_from_path(resolved_path_list);
        if not isinstance(node, dict) or 'children' not in node: raise NotADirectoryError(f"Не каталог: {path_str}")
        if not self._check_permission(node.get('meta'), 'r'): raise PermissionError(f"Отказано в доступе (чтение): {path_str}")
        content = []; children = node.get('children', {})
        for name, item in sorted(children.items()):
            meta = item.get('meta', {}); is_link = meta.get('is_link', False)
            item_type = "folder" if 'children' in item else ("link" if is_link else "file")
            item_size = ''; link_target = ''
            if item_type == "file":
                 try: item_size = len(item.get('content', '').encode('utf-8'))
                 except: item_size = len(item.get('content', ''))
            elif item_type == "link":
                 link_target = item.get('content', '');
                 try: item_size = len(link_target.encode('utf-8'))
                 except: item_size = len(link_target)
            elif item_type == "folder": item_size = meta.get('dir_size', 0)
            display_name = f"{name} -> {link_target}" if item_type == "link" else name
            content.append({'name': name, 'display_name': display_name, 'type': item_type, 'size': item_size,
                            'owner': meta.get('owner', '?'), 'permissions': meta.get('permissions', '---------'),
                            'mtime': meta.get('mtime'), 'ctime': meta.get('ctime'), # Добавлен ctime
                            'is_link': is_link, 'link_target': link_target})
        return content
    def do_cd_for_gui(self, target_dir):
        if not target_dir: return self.get_cwd_string()
        target_path_list = self._resolve_path(target_dir);
        if target_path_list is None: raise FileNotFoundError(f"Путь не найден: {target_dir}")
        node = self._get_node_from_path(target_path_list);
        if not isinstance(node, dict) or 'children' not in node: raise NotADirectoryError(f"Не каталог: {target_dir}")
        if not self._check_permission(node.get('meta'), 'x'): raise PermissionError(f"Отказано в доступе (выполнение): {target_dir}")
        self.current_working_directory = target_path_list; return self.get_cwd_string()
    def do_mkdir_internal(self, dir_path, owner, permissions):
         parent_node, dir_name, parent_path_list = self._get_parent_node_and_name(dir_path)
         if parent_node is None or dir_name is None: raise FileNotFoundError(f"Неверный путь или родительский каталог не существует: {dir_path}")
         self._create_node(parent_node, dir_name, 'folder', owner, permissions)
         self._update_directory_size(parent_path_list) # Обновляем размер родителя
    def do_mkdir_for_gui(self, dir_path):
        if not dir_path or dir_path.endswith('/'): raise ValueError(f"Некорректное имя каталога: {dir_path}")
        parent_node, dir_name, parent_path_list = self._get_parent_node_and_name(dir_path);
        if parent_node is None or dir_name is None: raise FileNotFoundError(f"Неверный путь или родительский каталог не существует: {dir_path}")
        parent_path_str = self.get_cwd_string() if parent_path_list == self.current_working_directory else '/' + '/'.join(parent_path_list[1:])
        if not self._check_permission(parent_node.get('meta'), 'w'): raise PermissionError(f"Отказано в доступе (запись): {parent_path_str}")
        default_perms = 'rwxr-xr-x'; self._create_node(parent_node, dir_name, 'folder', self.current_user, default_perms)
        self._update_directory_size(parent_path_list) # Обновляем размер родителя
    def do_ln_for_gui(self, target_path, link_path):
        if not link_path or link_path.endswith('/'): raise ValueError(f"Некорректное имя ссылки: {link_path}")
        resolved_target = self._resolve_path(target_path)
        if not resolved_target or self._get_node_from_path(resolved_target) is None: print(f"[ln] Предупреждение: Цель '{target_path}' не существует.")
        parent_node, link_name, parent_path_list = self._get_parent_node_and_name(link_path);
        if parent_node is None or link_name is None: raise FileNotFoundError(f"Неверный путь или родительский каталог не существует для ссылки: {link_path}")
        parent_path_str = self.get_cwd_string() if parent_path_list == self.current_working_directory else '/' + '/'.join(parent_path_list[1:])
        if not self._check_permission(parent_node.get('meta'), 'w'): raise PermissionError(f"Отказано в доступе (запись): {parent_path_str}")
        link_perms = 'rwxrwxrwx'; link_node = self._create_node(parent_node, link_name, 'file', self.current_user, link_perms, content=target_path)
        link_node['meta']['is_link'] = True
        self._update_directory_size(parent_path_list); print(f"[ln] Создана символическая ссылка '{link_path}' -> '{target_path}'")
    def do_touch_for_gui(self, file_path):
        if not file_path or file_path.endswith('/'): raise ValueError(f"Некорректное имя файла: {file_path}")
        parent_node, file_name, parent_path_list = self._get_parent_node_and_name(file_path);
        if parent_node is None or file_name is None: raise FileNotFoundError(f"Неверный путь или родительский каталог не существует: {file_path}")
        parent_path_str = self.get_cwd_string() if parent_path_list == self.current_working_directory else '/' + '/'.join(parent_path_list[1:])
        if not self._check_permission(parent_node.get('meta'), 'w'): raise PermissionError(f"Отказано в доступе (запись): {parent_path_str}")
        if file_name not in parent_node['children']:
            default_perms = 'rw-r--r--'; self._create_node(parent_node, file_name, 'file', self.current_user, default_perms, content="")
            self._update_directory_size(parent_path_list) # Обновляем размер родителя
        else:
            target_node = parent_node['children'][file_name]
            if not self._check_permission(target_node.get('meta'), 'w'): raise PermissionError(f"Отказано в доступе (запись): {file_path}")
            now = time.time(); target_node['meta']['mtime'] = now; parent_node['meta']['mtime'] = now
            # Размер не менялся, но на всякий случай можно обновить
            self._update_directory_size(parent_path_list)
    def do_rm_for_gui(self, path_to_remove):
        parent_node, name, parent_path_list = self._get_parent_node_and_name(path_to_remove);
        if parent_node is None or name is None: raise FileNotFoundError(f"Нет такого файла или каталога: {path_to_remove}")
        if name not in parent_node.get('children', {}): raise FileNotFoundError(f"Нет такого файла или каталога: {path_to_remove}")
        parent_path_str = self.get_cwd_string() if parent_path_list == self.current_working_directory else '/' + '/'.join(parent_path_list[1:])
        if not self._check_permission(parent_node.get('meta'), 'w'): raise PermissionError(f"Отказано в доступе (запись): {parent_path_str}")
        resolved_target_path = self._resolve_path(path_to_remove)
        if len(self.current_working_directory) >= len(resolved_target_path) and self.current_working_directory[:len(resolved_target_path)] == resolved_target_path:
             raise OSError(f"Нельзя удалить текущий каталог или его предка: {path_to_remove}")
        try:
            del parent_node['children'][name]; now = time.time(); parent_node['meta']['mtime'] = now
            self._update_directory_size(parent_path_list) # Обновляем размер родителя
        except Exception as e: raise OSError(f"Ошибка при удалении '{path_to_remove}': {e}")
    def read_file_for_gui(self, file_path):
        resolved_path_list = self._resolve_path(file_path);
        if resolved_path_list is None: raise FileNotFoundError(f"Путь не найден: {file_path}")
        node = self._get_node_from_path(resolved_path_list);
        if node is None: raise FileNotFoundError(f"Нет такого файла: {file_path}")
        if 'children' in node: raise IsADirectoryError(f"Это каталог: {file_path}")
        if not self._check_permission(node.get('meta'), 'r'): raise PermissionError(f"Отказано в доступе (чтение): {file_path}")
        return node.get('content', '')
    def write_file_for_gui(self, file_path, content, append=False):
         parent_node, file_name, parent_path_list = self._get_parent_node_and_name(file_path);
         if parent_node is None or file_name is None: raise FileNotFoundError(f"Неверный путь или родительский каталог не существует: {file_path}")
         target_node = parent_node.get('children', {}).get(file_name)
         if target_node is None: raise FileNotFoundError(f"Нет такого файла: {file_path}")
         if 'children' in target_node: raise IsADirectoryError(f"Не удается записать в каталог: {file_path}")
         if not self._check_permission(target_node.get('meta'), 'w'): raise PermissionError(f"Отказано в доступе (запись): {file_path}")
         existing_content = target_node.get('content', ''); new_content_str = ""
         if append: new_content_str = existing_content + content
         else: new_content_str = content
         current_size = self._calculate_fs_size(); old_file_size = len(existing_content.encode('utf-8'))
         new_file_size = len(new_content_str.encode('utf-8'))
         if current_size - old_file_size + new_file_size > self.max_fs_size: raise OSError("Недостаточно места на диске")
         target_node['content'] = new_content_str; now = time.time(); target_node['meta']['mtime'] = now; parent_node['meta']['mtime'] = now
         self._update_directory_size(parent_path_list) # Обновляем размер родителя
    def do_chmod_for_gui(self, path, mode_str):
        resolved_path_list = self._resolve_path(path);
        if resolved_path_list is None: raise FileNotFoundError(f"Путь не найден: {path}")
        node = self._get_node_from_path(resolved_path_list);
        if node is None: raise FileNotFoundError(f"Нет такого файла или каталога: {path}")
        meta = node.get('meta');
        if not meta: raise OSError("Не удалось получить метаданные узла")
        if self.current_user != meta.get('owner') and self.current_user != 'root': raise PermissionError(f"Операция не позволена: {path}")
        if not re.match("^[rwx-]{9}$", mode_str): raise ValueError(f"Некорректный формат прав: '{mode_str}'. Используйте 9 символов (r,w,x,-).")
        meta['permissions'] = mode_str; meta['mtime'] = time.time(); print(f"[chmod] Права для '{path}' изменены на {mode_str}")
    def do_rename_for_gui(self, old_path, new_name):
        if not new_name or '/' in new_name or '\\' in new_name: raise ValueError(f"Некорректное новое имя: '{new_name}'")
        parent_node, old_name, parent_path_list = self._get_parent_node_and_name(old_path);
        if parent_node is None or old_name is None: raise FileNotFoundError(f"Исходный путь не найден: {old_path}")
        if old_name not in parent_node.get('children', {}): raise FileNotFoundError(f"Исходный элемент не найден: {old_path}")
        parent_path_str = self.get_cwd_string() if parent_path_list == self.current_working_directory else '/' + '/'.join(parent_path_list[1:])
        if not self._check_permission(parent_node.get('meta'), 'w'): raise PermissionError(f"Отказано в доступе (запись в родительском каталоге): {parent_path_str}")
        if new_name in parent_node.get('children', {}): raise FileExistsError(f"Элемент с именем '{new_name}' уже существует.")
        try:
            node_to_rename = parent_node['children'].pop(old_name); parent_node['children'][new_name] = node_to_rename
            now = time.time(); parent_node['meta']['mtime'] = now
            # Размер родителя не меняется при переименовании, обновление не нужно
            # self._update_directory_size(parent_path_list)
            print(f"[rename] '{old_path}' переименован в '{new_name}'")
        except Exception as e:
            if old_name not in parent_node['children'] and new_name in parent_node['children']: parent_node['children'][old_name] = parent_node['children'].pop(new_name)
            raise OSError(f"Ошибка при переименовании: {e}")

    # --- Методы для процессов (остаются без изменений) ---
    def _add_process(self, command, user, cpu=None, ram=None):
        pid = self.next_pid; self.next_pid += 1
        if cpu is None: cpu = random.uniform(0.1, 1.5)
        if ram is None: ram = random.uniform(5, 25)
        self.processes[pid] = {'pid': pid, 'command': command, 'user': user, 'cpu': round(cpu, 1), 'ram': round(ram, 1)}
        print(f"[SimOS] Запущен процесс PID {pid}: {command} (User: {user}, CPU: {cpu:.1f}%, RAM: {ram:.1f}MB)"); return pid
    def get_process_list(self): return [p.copy() for p in self.processes.values()]
    def get_resource_summary(self):
        total_cpu_used = sum(p.get('cpu', 0) for p in self.processes.values()); total_ram_used = sum(p.get('ram', 0) for p in self.processes.values())
        max_cpu = self.total_cores * 100; cpu_percent = min(total_cpu_used, max_cpu)
        return {'total_cpu_percent': round(cpu_percent, 1), 'total_ram_used_mb': round(total_ram_used, 1), 'total_ram_mb': self.total_ram_mb, 'total_cores': self.total_cores}
    def kill_process(self, pid):
        if pid == 1: raise PermissionError(tr("taskmgr_kill_error_kernel"))
        process_info = self.processes.get(pid);
        if not process_info: raise ValueError(tr("taskmgr_kill_error_noexist", pid=pid))
        proc_owner = process_info.get('user')
        if self.current_user != 'root' and self.current_user != proc_owner: raise PermissionError(tr("taskmgr_kill_error_noperm"))
        del self.processes[pid]; print(f"[SimOS] Завершен процесс PID {pid}: {process_info.get('command')}"); return True

    # --- Методы для выполнения текстовых команд (остаются без изменений) ---
    def execute_text_command(self, command_line):
        """Выполняет текстовую команду, возвращает (stdout, stderr, exit_code)."""
        if not command_line.strip():
            return ("", "", 0)

        parts = command_line.split()
        command = parts[0].lower()
        args = parts[1:]

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        exit_code = 0

        if command in self.text_commands:
            try:
                # Вызываем соответствующий метод do_*_text
                exit_code = self.text_commands[command](args, stdout_buffer, stderr_buffer)
                # --- ИСПРАВЛЕНО: Эта строка теперь внутри try ---
                if exit_code is None: exit_code = 0 # По умолчанию успешный выход
            except PermissionError as e:
                print(f"PermissionError: {e}", file=stderr_buffer)
                exit_code = 1
            except (FileNotFoundError, NotADirectoryError, IsADirectoryError, FileExistsError) as e:
                print(f"{command}: {e}", file=stderr_buffer)
                exit_code = 1
            except ValueError as e: # Для ошибок аргументов и т.п.
                 print(f"{command}: {e}", file=stderr_buffer)
                 exit_code = 1
            except OSError as e: # Для ошибок диска, удаления и т.п.
                 print(f"{command}: {e}", file=stderr_buffer)
                 exit_code = 1
            except Exception as e:
                print(f"Непредвиденная ошибка выполнения '{command}': {e}", file=stderr_buffer)
                traceback.print_exc(file=stderr_buffer)
                exit_code = 2
        else:
            print(f"{command}: команда не найдена", file=stderr_buffer)
            exit_code = 127 # Стандартный код для "команда не найдена"

        return stdout_buffer.getvalue(), stderr_buffer.getvalue(), exit_code

    def do_pwd_text(self, args, stdout, stderr):
        if args: print("pwd: команда не принимает аргументов", file=stderr); return 1; print(self.get_cwd_string(), file=stdout); return 0
    def do_ls_text(self, args, stdout, stderr):
        path_to_list = self.get_cwd_string();
        if args: path_to_list = args[0]
        try: content = self.do_ls_for_gui(path_to_list); output = [item['name'] for item in content]; print("\n".join(output), file=stdout); return 0
        except Exception as e: raise e
    def do_cd_text(self, args, stdout, stderr):
        if not args: target_dir = self.users_info.get(self.current_user, {}).get('home', '/')
        else: target_dir = args[0]
        try: self.do_cd_for_gui(target_dir); return 0
        except Exception as e: raise e
    def do_mkdir_text(self, args, stdout, stderr):
        if not args: print("mkdir: укажите имя каталога", file=stderr); return 1
        try: self.do_mkdir_for_gui(args[0]); return 0
        except Exception as e: raise e
    def do_touch_text(self, args, stdout, stderr):
        if not args: print("touch: укажите имя файла", file=stderr); return 1
        try: self.do_touch_for_gui(args[0]); return 0
        except Exception as e: raise e
    def do_cat_text(self, args, stdout, stderr):
        if not args: print("cat: укажите имя файла", file=stderr); return 1
        exit_code = 0
        for file_path in args:
            try: content = self.read_file_for_gui(file_path); print(content, file=stdout, end='')
            except Exception as e: print(f"cat: {e}", file=stderr); exit_code = 1
        return exit_code
    def do_echo_text(self, args, stdout, stderr): print(*args, file=stdout); return 0
    def do_rm_text(self, args, stdout, stderr):
        if not args: print("rm: укажите имя файла или каталога", file=stderr); return 1
        exit_code = 0
        for path_to_remove in args:
             try: self.do_rm_for_gui(path_to_remove)
             except Exception as e: print(f"rm: {e}", file=stderr); exit_code = 1
        return exit_code
    def do_whoami_text(self, args, stdout, stderr):
        if args: print("whoami: команда не принимает аргументов", file=stderr); return 1; print(self.current_user, file=stdout); return 0
    def do_passwd_text(self, args, stdout, stderr):
        if len(args) != 1: print("Использование: passwd <новый_пароль>", file=stderr); return 1
        new_password = args[0]
        if self.set_user_password(self.current_user, new_password): print(f"Пароль для пользователя {self.current_user} успешно изменен.", file=stdout); return 0
        else: print(f"Ошибка: не удалось изменить пароль для {self.current_user}", file=stderr); return 1
    def do_adduser_text(self, args, stdout, stderr):
        if self.current_user != 'root': raise PermissionError("Только root может добавлять пользователей.")
        if len(args) != 2: print("Использование: adduser <имя_пользователя> <пароль>", file=stderr); return 1
        username, password = args[0], args[1]
        try: self.add_user(username, password); return 0
        except Exception as e: raise e
    def do_chmod_text(self, args, stdout, stderr):
        if len(args) != 2: print("Использование: chmod <права_rwx> <путь>", file=stderr); print("Пример: chmod rwxr-xr-- /home/guest/file.txt", file=stderr); return 1
        mode_str, path = args[0], args[1]
        try: self.do_chmod_for_gui(path, mode_str); return 0
        except Exception as e: raise e
    def do_help_text(self, args, stdout, stderr):
        print("Доступные команды терминала:", file=stdout); sorted_cmds = sorted(self.text_commands.keys())
        for cmd in sorted_cmds: print(f"  {cmd}", file=stdout); return 0
    def do_clear_text(self, args, stdout, stderr): return 0
    def do_exit_text(self, args, stdout, stderr): return -1

    def do_copy_for_gui(self, path_to_copy):
        """Копирует узел (файл/папку) и возвращает его копию и имя."""
        resolved_path_list = self._resolve_path(path_to_copy)
        if resolved_path_list is None: raise FileNotFoundError(f"Путь не найден: {path_to_copy}")
        if resolved_path_list == ['/']: raise ValueError("Нельзя копировать корневой каталог.")

        node = self._get_node_from_path(resolved_path_list)
        if node is None: raise FileNotFoundError(f"Элемент не найден: {path_to_copy}")

        # Проверка прав на чтение исходного элемента (и всех вложенных, если папка?)
        # Для простоты пока проверяем только сам узел
        if not self._check_permission(node.get('meta'), 'r'):
             raise PermissionError(f"Отказано в доступе (чтение): {path_to_copy}")

        original_name = resolved_path_list[-1]
        print(f"[Copy] Копирование узла: {original_name}")
        return copy.deepcopy(node), original_name

    def do_paste_for_gui(self, destination_dir_path, node_to_paste, original_name):
        """Вставляет скопированный узел в указанную директорию."""
        if node_to_paste is None: raise ValueError("Нет данных для вставки (буфер обмена пуст?).")

        dest_path_list = self._resolve_path(destination_dir_path)
        if dest_path_list is None: raise FileNotFoundError(f"Целевой каталог не найден: {destination_dir_path}")

        dest_node_parent = self._get_node_from_path(dest_path_list)
        if not dest_node_parent or 'children' not in dest_node_parent:
            raise NotADirectoryError(f"Целевой путь не является каталогом: {destination_dir_path}")

        if not self._check_permission(dest_node_parent.get('meta'), 'w'):
             raise PermissionError(f"Отказано в доступе (запись): {destination_dir_path}")

        new_name = original_name; counter = 1
        while new_name in dest_node_parent['children']:
            base, ext = os.path.splitext(original_name)
            new_name = f"{base}_copy{counter if counter > 1 else ''}{ext}"
            counter += 1
            if counter > 100: raise OSError("Слишком много копий с таким именем.")

        now = time.time()
        def update_meta_recursive(node, owner, current_time):
            if isinstance(node, dict) and 'meta' in node:
                node['meta']['owner'] = owner
                node['meta']['ctime'] = current_time
                node['meta']['mtime'] = current_time
                if 'dir_size' in node['meta']: node['meta']['dir_size'] = 0 # Сброс размера папки
                if 'children' in node:
                    for child in node['children'].values():
                        update_meta_recursive(child, owner, current_time)

        update_meta_recursive(node_to_paste, self.current_user, now)

        # Пересчитываем размер вставляемого узла (если папка)
        if 'children' in node_to_paste:
             self._update_directory_size_internal(node_to_paste) # Внутренний пересчет

        estimated_size = node_to_paste.get('meta', {}).get('dir_size', 0) if 'children' in node_to_paste else len(node_to_paste.get('content','').encode('utf-8'))
        current_fs_size = self._calculate_fs_size() # Полный пересчет для проверки лимита
        if current_fs_size + estimated_size > self.max_fs_size:
             raise OSError("Недостаточно места на диске для вставки.")

        dest_node_parent['children'][new_name] = node_to_paste
        dest_node_parent['meta']['mtime'] = now
        self._update_directory_size(dest_path_list) # Обновляем размер целевой папки

        print(f"[paste] Элемент '{original_name}' вставлен как '{new_name}' в '{destination_dir_path}'")
        return new_name

    def _update_directory_size_internal(self, node):
         """Внутренний метод для пересчета размера конкретного узла-папки."""
         if not node or 'children' not in node: return 0
         current_size = 0
         for child_name, child_node in node.get('children', {}).items():
             if 'children' in child_node: # Подпапка
                 current_size += self._update_directory_size_internal(child_node) # Рекурсивный вызов
             elif 'content' in child_node: # Файл
                 try: current_size += len(child_node.get('content', '').encode('utf-8'))
                 except: current_size += len(child_node.get('content', ''))
             current_size += 64 # Размер самого узла
         if 'meta' in node: node['meta']['dir_size'] = current_size
         return current_size + 64 # Возвращаем размер папки + ее собственный размер

    # --- НОВЫЙ МЕТОД ---
    def do_move_for_gui(self, source_path, destination_dir_path):
        """Перемещает файл/папку."""
        source_path_list = self._resolve_path(source_path)
        dest_dir_list = self._resolve_path(destination_dir_path)
        if source_path_list is None: raise FileNotFoundError(f"Источник не найден: {source_path}")
        if dest_dir_list is None: raise FileNotFoundError(f"Целевой каталог не найден: {destination_dir_path}")
        if source_path_list == ['/']: raise ValueError("Нельзя перемещать корневой каталог.")

        # Получаем узел источника и его родителя
        source_parent_node, source_name, source_parent_list = self._get_parent_node_and_name(source_path)
        if source_parent_node is None or source_name is None or source_name not in source_parent_node['children']:
             raise FileNotFoundError(f"Источник не найден: {source_path}")

        # Получаем узел назначения
        dest_node_parent = self._get_node_from_path(dest_dir_list)
        if not dest_node_parent or 'children' not in dest_node_parent:
            raise NotADirectoryError(f"Целевой путь не является каталогом: {destination_dir_path}")

        # Проверка прав: запись в исходном родителе И запись в целевом родителе
        source_parent_path_str = '/' + '/'.join(source_parent_list[1:]) if len(source_parent_list)>1 else '/'
        if not self._check_permission(source_parent_node.get('meta'), 'w'):
             raise PermissionError(f"Отказано в доступе (запись): {source_parent_path_str}")
        if not self._check_permission(dest_node_parent.get('meta'), 'w'):
             raise PermissionError(f"Отказано в доступе (запись): {destination_dir_path}")

        # Проверка конфликта имен
        new_name = source_name
        if new_name in dest_node_parent['children']:
            # Если перемещаем в ту же папку (переименование), это обрабатывается do_rename_for_gui
            if source_parent_list == dest_dir_list:
                 raise FileExistsError(f"Элемент с именем '{new_name}' уже существует (используйте переименование).")
            # Если перемещаем в другую папку и имя занято
            raise FileExistsError(f"Элемент с именем '{new_name}' уже существует в '{destination_dir_path}'.")

        # Проверка перемещения папки внутрь себя
        node_to_move = source_parent_node['children'][source_name]
        if 'children' in node_to_move: # Если это папка
             if len(dest_dir_list) >= len(source_path_list) and dest_dir_list[:len(source_path_list)] == source_path_list:
                  raise OSError(f"Нельзя переместить каталог '{source_path}' внутрь себя.")

        # Выполняем перемещение
        try:
            # Удаляем из старого места
            node_moved = source_parent_node['children'].pop(source_name)
            now = time.time()
            source_parent_node['meta']['mtime'] = now
            # Добавляем в новое место
            dest_node_parent['children'][new_name] = node_moved
            dest_node_parent['meta']['mtime'] = now
            # Обновляем время модификации самого узла (опционально)
            if 'meta' in node_moved: node_moved['meta']['mtime'] = now

            # Обновляем размеры папок
            self._update_directory_size(source_parent_list)
            if source_parent_list != dest_dir_list: # Обновляем целевую, только если она другая
                 self._update_directory_size(dest_dir_list)

            print(f"[move] Элемент '{source_path}' перемещен в '{destination_dir_path}'")
            return new_name
        except Exception as e:
            # Попытка отката (очень простая)
            if source_name not in source_parent_node['children'] and new_name in dest_node_parent['children']:
                 source_parent_node['children'][source_name] = dest_node_parent['children'].pop(new_name)
            raise OSError(f"Ошибка при перемещении: {e}")




class LoginWindow(tk.Toplevel):
    """Окно входа в систему с проверкой пароля."""
    def __init__(self, parent, sim_os_instance, callback_on_success):
        super().__init__(parent)
        self.parent = parent
        self.sim_os = sim_os_instance
        self.callback = callback_on_success
        # self.correct_password = "1234" # Убрали фиксированный пароль

        self.title("Вход в SimOS")
        self.geometry("300x170")
        self.resizable(False, False)
        # self.grab_set() # Убрали для совместимости
        # self.transient(parent) # Убрали для совместимости

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(main_frame, text="Имя пользователя:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.username_entry.insert(0, "guest")
        ttk.Label(main_frame, text="Пароль:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.error_label = ttk.Label(main_frame, text="", foreground="red")
        self.error_label.grid(row=2, column=0, columnspan=2, pady=(0, 5))
        login_button = ttk.Button(main_frame, text="Войти", command=self.attempt_login)
        login_button.grid(row=3, column=0, columnspan=2, pady=5)
        main_frame.grid_columnconfigure(1, weight=1)
        self.username_entry.focus_set()
        self.password_entry.bind("<Return>", self.attempt_login)
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def attempt_login(self, event=None):
        """Проверяет учетные данные и пароль (с хэшем)."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.error_label.config(text="")

        if username not in self.sim_os.users_info:
            self.error_label.config(text=f"Пользователь '{username}' не найден.")
            return

        # Используем метод SimOS для проверки пароля
        if self.sim_os.verify_user_password(username, password):
            self.sim_os.current_user = username
            # self.grab_release() # Убрали
            self.destroy()
            self.callback()
        else:
            self.error_label.config(text="Неверный пароль.")
            self.password_entry.delete(0, tk.END)

    def update_language(self):
        self.title(tr("login_title"))
        # Находим виджеты и обновляем их текст (нужно будет сохранить ссылки на них в self)
        # Пример (предполагается, что метки сохранены в self.user_lbl, self.pass_lbl, self.login_btn):
        # self.user_lbl.config(text=tr("username_label"))
        # self.pass_lbl.config(text=tr("password_label"))
        # self.login_btn.config(text=tr("login_button"))
        # Проще пересоздать виджеты или хранить ссылки на них при инициализации
        # Пока оставим заглушку, т.к. окно логина обычно не меняет язык "на лету"
        print("[LoginWindow] update_language called (stub)")


    def on_close(self):
        self.parent.destroy()


class DesktopWindow:
    """Основное окно рабочего стола с иконками, панелью задач, обоями и перетаскиванием."""
    ICON_SIZE = 48
    ICON_GRID_PADDING_X = 90
    ICON_GRID_PADDING_Y = 100
    ICON_GRID_START_X = 40
    ICON_GRID_START_Y = 40
    RESIZE_DEBOUNCE_MS = 250
    TASKBAR_ICON_SIZE = (20, 20)
    MENU_ICON_SIZE = (16, 16)

    def __init__(self, root, sim_os_instance):
        self.root = root
        self.sim_os = sim_os_instance
        self.root.config(bg=self.sim_os.desktop_bg_color)
        self.root.title(tr("desktop_title", os_name=self.sim_os.os_name, user=self.sim_os.current_user))
        self.root.geometry("800x600")
        self.open_windows = {}
        self.current_lang = "RU"
        self.icon_cache = {}
        self.taskbar_icon_cache = {}
        self._wallpaper_photo = None
        self._wallpaper_id = None
        self._resize_after_id = None
        self._desktop_icon_items = {} # {app_name: {'ids': [id1, id2..], 'x': x, 'y': y, 'tag': tag}}
        self._drag_data = {"x": 0, "y": 0, "item": None, "app_name": None} # Для перетаскивания

        # --- Меню ---
        menubar = tk.Menu(self.root); self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0); menubar.add_cascade(label=tr("file_menu"), menu=file_menu)
        file_menu.add_command(label=tr("save_state_menu"), command=self.sim_os.save_state); file_menu.add_separator(); file_menu.add_command(label=tr("exit_menu"), command=self.on_close)
        apps_menu = tk.Menu(menubar, tearoff=0); menubar.add_cascade(label=tr("apps_menu"), menu=apps_menu)
        apps_menu.add_command(label=tr("explorer_app"), command=self.launch_explorer); apps_menu.add_command(label=tr("calculator_app"), command=self.launch_calculator); apps_menu.add_command(label=tr("terminal_app"), command=self.launch_terminal)
        apps_menu.add_command(label=tr("editor_app"), command=self.launch_editor) # Добавлен Редактор
        apps_menu.add_separator(); apps_menu.add_command(label=tr("settings_app"), command=self.launch_settings); apps_menu.add_command(label=tr("taskmgr_app"), command=self.launch_task_manager)

        # --- Панель задач ---
        self.taskbar_frame = tk.Frame(self.root, height=35, bg="#cccccc", relief=tk.RAISED, borderwidth=1)
        self.taskbar_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.taskbar_frame.pack_propagate(False)
        self.create_taskbar_elements() # Создаем ДО Canvas

        # --- Canvas для рабочего стола ---
        self.desktop_canvas = tk.Canvas(self.root, bg=self.sim_os.desktop_bg_color, highlightthickness=0)
        self.desktop_canvas.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # --- Привязки событий для перетаскивания на Canvas ---
        self.desktop_canvas.tag_bind("icon", "<ButtonPress-1>", self.on_icon_press)
        self.desktop_canvas.tag_bind("icon", "<B1-Motion>", self.on_icon_drag)
        self.desktop_canvas.tag_bind("icon", "<ButtonRelease-1>", self.on_icon_release)

        # --- Загружаем обои и создаем иконки ---
        self.root.after(10, self._update_wallpaper_debounced)
        self.root.after(20, self.create_desktop_icons) # Рисуем иконки

        # --- Привязки событий окна ---
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.bind("<Configure>", self._on_window_resize_schedule)
        # Горячие клавиши
        self.root.bind("<Control-e>", lambda event: self.launch_explorer())
        self.root.bind("<Control-k>", lambda event: self.launch_calculator())
        self.root.bind("<Control-t>", lambda event: self.launch_terminal())
        self.root.bind("<Control-p>", lambda event: self.launch_settings())
        self.root.bind("<Control-Shift-Escape>", lambda event: self.launch_task_manager())
        self.root.bind("<Control-Alt-T>", lambda event: self.launch_editor()) # Пример для редактора
        self.root.bind("<Control-g>", lambda event: self.launch_snake_game())
        print("[Desktop] Инициализация завершена.")

    # --- Методы on_close, _load_icon, _on_window_resize_schedule, _update_wallpaper_debounced, _update_wallpaper ---
    # --- ОСТАЮТСЯ БЕЗ ИЗМЕНЕНИЙ (скопируйте их из предыдущей версии) ---
    def on_close(self):
        if self._resize_after_id: self.root.after_cancel(self._resize_after_id); self._resize_after_id = None
        if messagebox.askokcancel(tr("exit_prompt_title"), tr("exit_prompt_message"), parent=self.root):
             self.sim_os.save_state()
        self.root.destroy()

    def _load_icon(self, relative_icon_path, size=None, cache=None, is_wallpaper=False):
        """Вспомогательная функция для загрузки и кэширования иконок/обоев."""
        if cache is None: cache = self.icon_cache

        # --- Получаем абсолютный путь с помощью resource_path ---
        absolute_path = resource_path(relative_icon_path)
        # --- Конец ---

        # Для обоев не используем кэш PhotoImage, т.к. размер меняется
        use_photo_cache = (cache is self.icon_cache) and not is_wallpaper and size == (self.ICON_SIZE, self.ICON_SIZE)

        # Ключом кэша делаем относительный путь
        cache_key = relative_icon_path
        if use_photo_cache and cache_key in cache: return cache[cache_key]

        try:
            # --- Открываем по абсолютному пути ---
            img = Image.open(absolute_path)
            # --- Конец ---
            if is_wallpaper: return img
            else:
                 if size: img.thumbnail(size, Image.Resampling.LANCZOS)
                 photo_img = ImageTk.PhotoImage(img)
                 if use_photo_cache: cache[cache_key] = photo_img
                 return photo_img
        except FileNotFoundError:
            print(f"Предупреждение: Файл не найден: {absolute_path}") # Печатаем абсолютный путь для отладки
            return None
        except Exception as e:
            print(f"Ошибка загрузки {absolute_path}: {e}") # Печатаем абсолютный путь для отладки
            return None


    def _on_window_resize_schedule(self, event=None):
        if self._resize_after_id: self.root.after_cancel(self._resize_after_id)
        self._resize_after_id = self.root.after(self.RESIZE_DEBOUNCE_MS, self._update_wallpaper_debounced)

    def _update_wallpaper_debounced(self):
        self._resize_after_id = None; print("[Wallpaper] Debounced update triggered.")
        self._update_wallpaper(); self.create_desktop_icons()

    def _update_wallpaper(self):
         try:
             width = self.desktop_canvas.winfo_width(); height = self.desktop_canvas.winfo_height()
             if width <= 1 or height <= 1: return
             print(f"[Wallpaper] Updating wallpaper for size {width}x{height}")
             wallpaper_img = self._load_icon(self.sim_os.desktop_wallpaper_path, is_wallpaper=True)
             if wallpaper_img:
                 img_copy = wallpaper_img.copy(); img_resized = img_copy.resize((width, height), Image.Resampling.LANCZOS)
                 self._wallpaper_photo = ImageTk.PhotoImage(img_resized)
                 if self._wallpaper_id: self.desktop_canvas.delete(self._wallpaper_id)
                 self._wallpaper_id = self.desktop_canvas.create_image(0, 0, anchor='nw', image=self._wallpaper_photo)
                 self.desktop_canvas.tag_lower(self._wallpaper_id); self.desktop_canvas.config(bg=self.sim_os.desktop_bg_color)
                 print("[Wallpaper] Wallpaper updated successfully.")
             else:
                 self.desktop_canvas.config(bg=self.sim_os.desktop_bg_color)
                 if self._wallpaper_id: self.desktop_canvas.delete(self._wallpaper_id); self._wallpaper_id = None
                 self._wallpaper_photo = None; print("[Wallpaper] Failed to load wallpaper, using background color.")
         except Exception as e:
             print(f"Ошибка обновления обоев: {e}"); traceback.print_exc()
             self.desktop_canvas.config(bg=self.sim_os.desktop_bg_color)
             if self._wallpaper_id: self.desktop_canvas.delete(self._wallpaper_id); self._wallpaper_id = None
             self._wallpaper_photo = None

    # --- Методы для перетаскивания иконок ---
    def on_icon_press(self, event):
        """Начало перетаскивания иконки."""
        # Находим элемент Canvas под курсором с тегом 'icon'
        item_id = self.desktop_canvas.find_closest(event.x, event.y)[0]
        tags = self.desktop_canvas.gettags(item_id)
        if "icon" in tags:
            # Находим основной тег иконки (icon_appname)
            icon_tag = next((tag for tag in tags if tag.startswith("icon_")), None)
            if icon_tag:
                self._drag_data["item"] = icon_tag # Сохраняем тег группы
                self._drag_data["x"] = event.x
                self._drag_data["y"] = event.y
                self._drag_data["app_name"] = icon_tag.split("_", 1)[1]
                # Поднимаем все элементы иконки наверх
                self.desktop_canvas.tag_raise(icon_tag)
                print(f"Dragging started for: {self._drag_data['app_name']}")

    def on_icon_drag(self, event):
        """Перемещение иконки во время перетаскивания."""
        if self._drag_data["item"]:
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]
            # Перемещаем все элементы с этим тегом
            self.desktop_canvas.move(self._drag_data["item"], dx, dy)
            # Обновляем начальные координаты для следующего шага
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

    def on_icon_release(self, event):
        """Завершение перетаскивания иконки."""
        if self._drag_data["item"] and self._drag_data["app_name"]:
            app_name = self._drag_data["app_name"]
            # Получаем новые координаты верхнего левого угла (приблизительно)
            # Ищем ID изображения иконки
            icon_info = self._desktop_icon_items.get(app_name)
            if icon_info:
                 try:
                     coords = self.desktop_canvas.coords(icon_info['image'])
                     if coords:
                         new_x, new_y = int(coords[0]), int(coords[1])
                         # Сохраняем новую позицию
                         self.sim_os.desktop_icon_positions[app_name] = (new_x, new_y)
                         print(f"Dragging finished for {app_name} at ({new_x}, {new_y})")
                 except tk.TclError:
                      print(f"Warning: Could not get coords for icon {app_name} after drag.")
                 except Exception as e:
                      print(f"Error getting coords after drag: {e}")

        # Сбрасываем данные перетаскивания
        self._drag_data = {"x": 0, "y": 0, "item": None, "app_name": None}

    # --- Переработанный метод create_desktop_icon ---
    def create_desktop_icon(self, app_name, text, image_path, command, x, y):
        """Рисует иконку (изображение + текст) прямо на Canvas."""
        icon_text_bg_color = ""
        photo_img = self._load_icon(image_path, size=(self.ICON_SIZE, self.ICON_SIZE), cache=self.icon_cache)
        icon_tag = f"icon_{app_name}"

        # Удаляем предыдущие элементы этой иконки, если они есть
        self.desktop_canvas.delete(icon_tag)

        if photo_img:
            img_id = self.desktop_canvas.create_image(x, y, anchor='nw', image=photo_img, tags=("icon", icon_tag))
        else:
            img_id = self.desktop_canvas.create_rectangle(x, y, x + self.ICON_SIZE, y + self.ICON_SIZE, fill="red", outline="black", tags=("icon", icon_tag))
            self.desktop_canvas.create_text(x + self.ICON_SIZE / 2, y + self.ICON_SIZE / 2, text="X", fill="white", font=("Arial", 16, "bold"), tags=("icon", icon_tag))

        text_y = y + self.ICON_SIZE + 5
        text_id = self.desktop_canvas.create_text(
            x + self.ICON_SIZE / 2, text_y, anchor='n', text=text, fill="white",
            font=("Arial", 8), width=self.ICON_GRID_PADDING_X - 10,
            justify=tk.CENTER, tags=("icon", icon_tag)
        )
        # Привязываем событие клика ко всем элементам иконки (по тегу)
        self.desktop_canvas.tag_bind(icon_tag, "<Button-1>", lambda event, cmd=command: cmd())
        # Сохраняем ID элементов и координаты
        self._desktop_icon_items[app_name] = {'ids': self.desktop_canvas.find_withtag(icon_tag), 'x': x, 'y': y, 'tag': icon_tag, 'image': img_id, 'text': text_id}

    # --- Переработанный метод create_desktop_icons ---
    def create_desktop_icons(self):
        """Размещает иконки приложений на Canvas, используя сохраненные или стандартные позиции."""
        self.desktop_canvas.delete("icon")  # Удаляем все старые элементы иконок
        self._desktop_icon_items = {}  # Очищаем словарь ID

        # --- Список приложений с их данными ---
        apps = [
            ("explorer", tr("explorer_app"), "icons/explorer.png", self.launch_explorer),
            ("calculator", tr("calculator_app"), "icons/calculator.png", self.launch_calculator),
            ("terminal", tr("terminal_app"), "icons/terminal.png", self.launch_terminal),
            ("settings", tr("settings_app"), "icons/settings.png", self.launch_settings),
            ("taskmanager", tr("taskmgr_app"), "icons/task_manager.png", self.launch_task_manager),
            ("editor", tr("editor_app"), "icons/editor.png", self.launch_editor),
            ("snake", tr("snake_app"), "icons/snake_game.png", self.launch_snake_game),  # Добавлена Змейка
            # Добавьте сюда другие приложения
        ]
        # --- Конец списка приложений ---

        row, col = 0, 0
        canvas_width = self.desktop_canvas.winfo_width()
        # Если ширина еще не определена, используем размер окна по умолчанию
        if canvas_width <= 1: canvas_width = self.root.winfo_width()
        if canvas_width <= 1: canvas_width = 800  # Фоллбэк

        # Рассчитываем максимальное количество колонок
        max_cols = max(1, (canvas_width - self.ICON_GRID_START_X) // self.ICON_GRID_PADDING_X)

        for app_name, text, img_path, cmd in apps:
            # Получаем сохраненную позицию или вычисляем стандартную
            saved_pos = self.sim_os.desktop_icon_positions.get(app_name)
            if saved_pos:
                x, y = saved_pos
                # Проверяем, не выходит ли сохраненная позиция за пределы видимой области
                # (простая проверка, можно улучшить)
                if x > canvas_width - self.ICON_SIZE or y > self.desktop_canvas.winfo_height() - self.ICON_SIZE:
                    print(f"Предупреждение: Сохраненная позиция для {app_name} вне видимой области, сброс.")
                    x = self.ICON_GRID_START_X + col * self.ICON_GRID_PADDING_X
                    y = self.ICON_GRID_START_Y + row * self.ICON_GRID_PADDING_Y
                    self.sim_os.desktop_icon_positions[app_name] = (x, y)  # Обновляем сохраненную
                    col += 1
                    if col >= max_cols: col = 0; row += 1
            else:
                # Вычисляем стандартную позицию
                x = self.ICON_GRID_START_X + col * self.ICON_GRID_PADDING_X
                y = self.ICON_GRID_START_Y + row * self.ICON_GRID_PADDING_Y
                # Сохраняем стандартную позицию для будущего использования
                self.sim_os.desktop_icon_positions[app_name] = (x, y)
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

            # --- ВЫЗЫВАЕМ МЕТОД ДЛЯ СОЗДАНИЯ ОДНОЙ ИКОНКИ ---
            self.create_desktop_icon(app_name, text, img_path, cmd, x, y)


    def create_taskbar_elements(self):
        """Создает элементы на панели задач, включая закрепленные иконки."""
        # Очищаем старые элементы панели задач (кроме самой панели)
        for widget in self.taskbar_frame.winfo_children():
            widget.destroy()

        # --- Кнопка "Пуск" ---
        start_icon_path = "icons/start_icon.png"
        start_photo = self._load_icon(start_icon_path, size=self.TASKBAR_ICON_SIZE, cache=self.taskbar_icon_cache)
        start_button = tk.Button(self.taskbar_frame, image=start_photo, relief=tk.RAISED, borderwidth=2, command=self.show_start_menu)
        if start_photo: start_button.image = start_photo
        else: start_button.config(text=tr("start_button"), width=6)
        start_button.pack(side=tk.LEFT, padx=5, pady=3)

        # --- Область для иконок приложений (закрепленных и открытых) ---
        self.app_icon_frame = tk.Frame(self.taskbar_frame, bg=self.taskbar_frame.cget('bg'))
        self.app_icon_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.app_icon_frame.bind("<Button-3>", self.handle_taskbar_right_click)

        # --- Отображаем закрепленные и открытые приложения ---
        self.update_taskbar_app_icons()

        # --- Элементы справа ---
        self.lang_label = tk.Label(self.taskbar_frame, text=self.current_lang, bg=self.taskbar_frame.cget('bg'), fg="black", relief=tk.SUNKEN, borderwidth=1, padx=4)
        self.lang_label.pack(side=tk.RIGHT, padx=5, pady=3)
        self.lang_label.bind("<Button-1>", self.toggle_language)
        self.time_label = tk.Label(self.taskbar_frame, text="", bg=self.taskbar_frame.cget('bg'), fg="black", justify=tk.RIGHT)
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=3)
        self.update_time()

    # --- НОВЫЙ МЕТОД ---
    def update_taskbar_app_icons(self):
        """Обновляет иконки приложений на панели задач (закрепленные и открытые)."""
        # Очищаем текущие кнопки приложений
        for widget in self.app_icon_frame.winfo_children():
            widget.destroy()

        # Создаем кнопки для закрепленных и открытых приложений
        displayed_apps = set()

        # Сначала закрепленные
        for app_name in self.sim_os.pinned_apps:
            if app_name not in displayed_apps:
                self._create_or_update_taskbar_button(app_name)
                displayed_apps.add(app_name)

        # Затем открытые (которые еще не отображены)
        for app_name in self.open_windows:
            if app_name not in displayed_apps:
                self._create_or_update_taskbar_button(app_name)
                # displayed_apps.add(app_name) # Не нужно, т.к. open_windows уникальны

    # --- НОВЫЙ МЕТОД ---
    def _create_or_update_taskbar_button(self, app_name):
         """Создает или обновляет кнопку приложения на панели задач."""
         app_info = self._get_app_info(app_name)
         if not app_info: return

         icon_path = app_info["icon"]
         taskbar_icon_photo = self._load_icon(icon_path, size=self.TASKBAR_ICON_SIZE, cache=self.taskbar_icon_cache)

         # Проверяем, есть ли уже кнопка для этого открытого окна
         existing_button = self.open_windows.get(app_name, {}).get('taskbar_button')

         if existing_button and existing_button.winfo_exists():
              # Кнопка уже есть (окно открыто), просто убедимся, что иконка актуальна
              if taskbar_icon_photo:
                   existing_button.config(image=taskbar_icon_photo)
                   existing_button.image = taskbar_icon_photo
              return existing_button # Возвращаем существующую кнопку
         else:
              # Создаем новую кнопку (для закрепленного или нового окна)
              # Используем ttk.Button для лучшего вида с темами
              taskbar_button = ttk.Button(self.app_icon_frame, image=taskbar_icon_photo,
                                          command=lambda name=app_name: self.handle_taskbar_click(name))
              if taskbar_icon_photo:
                   taskbar_button.image = taskbar_icon_photo
              else: # Заглушка текстом
                   taskbar_button.config(text=app_name[:3]) # Первые 3 буквы имени
              taskbar_button.pack(side=tk.LEFT, padx=2, pady=2)
              # Привязка правого клика теперь делается на родительский фрейм
              return taskbar_button

    def update_time(self):
        now_str = time.strftime("%H:%M:%S\n%d.%m.%Y"); self.time_label.config(text=now_str)
        if self.root.winfo_exists(): self.root.after(1000, self.update_time)

    def toggle_language(self, event=None):
        self.current_lang = "EN" if self.current_lang == "RU" else "RU"; self.lang_label.config(text=self.current_lang); self.update_language()

    def update_language(self):
        global current_language; current_language = self.current_lang
        self.root.title(tr("desktop_title", os_name=self.sim_os.os_name, user=self.sim_os.current_user))
        menubar = tk.Menu(self.root); self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0); menubar.add_cascade(label=tr("file_menu"), menu=file_menu)
        file_menu.add_command(label=tr("save_state_menu"), command=self.sim_os.save_state); file_menu.add_separator(); file_menu.add_command(label=tr("exit_menu"), command=self.on_close)
        apps_menu = tk.Menu(menubar, tearoff=0); menubar.add_cascade(label=tr("apps_menu"), menu=apps_menu)
        apps_menu.add_command(label=tr("explorer_app"), command=self.launch_explorer); apps_menu.add_command(label=tr("calculator_app"), command=self.launch_calculator); apps_menu.add_command(label=tr("terminal_app"), command=self.launch_terminal)
        apps_menu.add_command(label=tr("editor_app"), command=self.launch_editor) # Добавлен Редактор
        apps_menu.add_command(label=tr("snake_app"), command=self.launch_snake_game)
        apps_menu.add_separator(); apps_menu.add_command(label=tr("settings_app"), command=self.launch_settings); apps_menu.add_command(label=tr("taskmgr_app"), command=self.launch_task_manager)
        self.create_desktop_icons()
        for app_name, info in list(self.open_windows.items()):
            if info['window'].winfo_exists():
                try:
                    app_info = self._get_app_info(app_name); title_key = app_info["title_key"]
                    title_args = {'user': self.sim_os.current_user} if title_key == "terminal_title" else {}
                    info['window'].title(tr(title_key, **title_args))
                    info['window'].update_language()
                except AttributeError: print(f"Предупреждение: у окна {app_name} нет метода update_language()")
                except Exception as e: print(f"Ошибка при обновлении языка окна {app_name}: {e}")
        print(f"[Desktop] Язык обновлен на {self.current_lang}")

    # --- Переработанный метод show_start_menu ---
    def show_start_menu(self):
        """Показывает улучшенное меню 'Пуск'."""
        start_menu = tk.Menu(self.root, tearoff=0)

        # --- Подменю Приложения ---
        apps_submenu = tk.Menu(start_menu, tearoff=0)
        apps_list = [
            (tr("explorer_app"), self.launch_explorer, "icons/explorer.png"),
            (tr("calculator_app"), self.launch_calculator, "icons/calculator.png"),
            (tr("terminal_app"), self.launch_terminal, "icons/terminal.png"),
            (tr("editor_app"), self.launch_editor, "icons/editor.png"),
            (tr("snake_app"), self.launch_snake_game, "icons/snake_game.png"),
        ]
        for label, cmd, icon_path in apps_list:
            icon = self._load_icon(icon_path, size=self.MENU_ICON_SIZE, cache=self.taskbar_icon_cache)
            apps_submenu.add_command(label=label, image=icon, compound=tk.LEFT, command=cmd)
            if icon: apps_submenu.entryconfigure(apps_submenu.index(tk.END), image=icon)
        start_menu.add_cascade(label=tr("start_menu_apps"), menu=apps_submenu)

        # --- Подменю Система ---
        system_submenu = tk.Menu(start_menu, tearoff=0)
        system_list = [
             (tr("settings_app"), self.launch_settings, "icons/settings.png"),
             (tr("taskmgr_app"), self.launch_task_manager, "icons/task_manager.png"),
        ]
        for label, cmd, icon_path in system_list:
            icon = self._load_icon(icon_path, size=self.MENU_ICON_SIZE, cache=self.taskbar_icon_cache)
            system_submenu.add_command(label=label, image=icon, compound=tk.LEFT, command=cmd)
            if icon: system_submenu.entryconfigure(system_submenu.index(tk.END), image=icon)
        start_menu.add_cascade(label=tr("start_menu_system"), menu=system_submenu)

        start_menu.add_separator()
        start_menu.add_command(label=tr("start_menu_exit"), command=self.on_close)

        start_button = self.taskbar_frame.winfo_children()[0]; x = start_button.winfo_rootx(); y = start_button.winfo_rooty() - start_menu.winfo_reqheight()
        try: start_menu.tk_popup(x, y)
        finally: start_menu.grab_release()

    def handle_taskbar_right_click(self, event):
         """Обрабатывает правый клик на области иконок панели задач."""
         clicked_widget = event.widget.winfo_containing(event.x_root, event.y_root)
         target_button = None
         # Ищем кнопку, на которую кликнули
         while clicked_widget and clicked_widget != self.app_icon_frame:
              if isinstance(clicked_widget, (ttk.Button, tk.Button)):
                   target_button = clicked_widget
                   break
              clicked_widget = clicked_widget.master

         if target_button:
             # Ищем app_name, связанный с этой кнопкой
             found_app_name = None
             for app_name, info in self.open_windows.items():
                 if info.get('taskbar_button') == target_button:
                     found_app_name = app_name
                     break
             # Если не нашли среди открытых, ищем среди закрепленных (по иконке?) - сложнее
             # Пока работаем только с открытыми
             if found_app_name:
                 self.show_taskbar_context_menu(event, found_app_name)

    # --- Переработанный метод show_taskbar_context_menu ---
    def show_taskbar_context_menu(self, event, app_name):
        """Показывает контекстное меню для кнопки на панели задач."""
        context_menu = tk.Menu(self.root, tearoff=0)

        # Команда Активировать (если окно существует)
        if app_name in self.open_windows and self.open_windows[app_name]['window'].winfo_exists():
            context_menu.add_command(label=tr("taskbar_activate"), command=lambda name=app_name: self.handle_taskbar_click(name))
        else: # Если окно закрыто (но кнопка закреплена)
             app_info = self._get_app_info(app_name)
             if app_info: # Добавляем команду для запуска
                  context_menu.add_command(label=tr(app_info["title_key"]), command=lambda name=app_name: self.launch_app(name))


        # Команда Закрепить/Открепить
        if app_name in self.sim_os.pinned_apps:
            context_menu.add_command(label=tr("taskbar_unpin"), command=lambda name=app_name: self.toggle_pin_app(name))
        else:
            context_menu.add_command(label=tr("taskbar_pin"), command=lambda name=app_name: self.toggle_pin_app(name))

        # Команда Закрыть (если окно открыто)
        if app_name in self.open_windows and self.open_windows[app_name]['window'].winfo_exists():
            context_menu.add_separator()
            context_menu.add_command(label=tr("taskbar_close"), command=lambda name=app_name: self.close_app_window(name))

        try: context_menu.tk_popup(event.x_root, event.y_root)
        finally: context_menu.grab_release()

    # --- НОВЫЙ МЕТОД ---
    def toggle_pin_app(self, app_name):
        """Закрепляет или открепляет приложение."""
        if app_name in self.sim_os.pinned_apps:
            self.sim_os.pinned_apps.remove(app_name)
            print(f"[Taskbar] Приложение '{app_name}' откреплено.")
            # Если окно не открыто, удаляем кнопку
            if app_name not in self.open_windows:
                 self.remove_taskbar_button(app_name) # Удаляем кнопку, если она была только из-за закрепления
        else:
            # Добавляем в начало списка закрепленных
            self.sim_os.pinned_apps.insert(0, app_name)
            print(f"[Taskbar] Приложение '{app_name}' закреплено.")
            # Обновляем панель задач, чтобы кнопка появилась, если ее не было
            self.update_taskbar_app_icons()
        # В любом случае обновляем панель задач, чтобы кнопки перерисовались в нужном порядке
        self.update_taskbar_app_icons()


    def handle_taskbar_click(self, app_name):
        """Обрабатывает клик по кнопке на панели задач (активирует или запускает)."""
        if app_name in self.open_windows and self.open_windows[app_name]['window'].winfo_exists():
            win = self.open_windows[app_name]['window']
            try:
                if win.state() == 'iconic': win.deiconify()
                win.lift(); win.focus_force()
            except tk.TclError: pass
        else:
            # Если окна нет, но кнопка есть (закреплена), запускаем приложение
            self.launch_app(app_name) # Используем launch_app, который обработает все сам

    def close_app_window(self, app_name, pid_to_kill=None):
        """Закрывает окно приложения, удаляет кнопку (если не закреплена) и имитирует завершение процесса."""
        print(f"[Desktop] Закрытие окна для {app_name}")
        if app_name in self.open_windows:
            win_info = self.open_windows[app_name]
            if pid_to_kill is None: pid_to_kill = win_info.get('pid')
            if pid_to_kill:
                 try:
                      if pid_to_kill in self.sim_os.processes:
                           del self.sim_os.processes[pid_to_kill]
                           print(f"[SimOS] Завершен процесс PID {pid_to_kill} (закрытие окна {app_name})")
                 except Exception as e: print(f"Ошибка при попытке убить процесс {pid_to_kill} для {app_name}: {e}")

            if win_info['window'].winfo_exists(): win_info['window'].destroy()
            # Удаляем кнопку только если приложение НЕ закреплено
            if app_name not in self.sim_os.pinned_apps:
                 self.remove_taskbar_button(app_name)
            # Удаляем запись об открытом окне в любом случае
            if app_name in self.open_windows:
                 del self.open_windows[app_name]


    def remove_taskbar_button(self, app_name):
         """Удаляет кнопку с панели задач (если она не нужна для закрепления)."""
         # Этот метод теперь не нужен, т.к. кнопки управляются в update_taskbar_app_icons
         # Оставим его пустым или удалим вызовы к нему
         # Вместо него нужно вызвать self.update_taskbar_app_icons()
         self.update_taskbar_app_icons()
         print(f"[Desktop] Запрос на удаление кнопки для {app_name} (обновление панели)")


    def _get_app_info(self, app_name):
        """Возвращает информацию о приложении."""
        app_registry = {
            "explorer": {"class": FileExplorerWindow, "icon": "icons/explorer.png", "title_key": "explorer_title"},
            "calculator": {"class": CalculatorWindow, "icon": "icons/calculator.png", "title_key": "calculator_title"},
            "terminal": {"class": TerminalWindow, "icon": "icons/terminal.png", "title_key": "terminal_title"},
            "settings": {"class": SettingsWindow, "icon": "icons/settings.png", "title_key": "settings_title"},
            "taskmanager": {"class": TaskManagerWindow, "icon": "icons/task_manager.png", "title_key": "taskmgr_title"},
            "editor": {"class": TextEditorWindow, "icon": "icons/editor.png", "title_key": "editor_app"},
            "snake": {"class": SnakeGameWindow, "icon": "icons/snake_game.png", "title_key": "snake_app"}, # Добавлена Змейка
        }
        return app_registry.get(app_name)

    def launch_app(self, app_name, *args):
        """Общий метод для запуска приложений, управления окнами и панелью задач."""
        app_info = self._get_app_info(app_name)
        if not app_info: print(f"Ошибка: Неизвестное приложение '{app_name}'"); return

        window_class = app_info["class"]; icon_path = app_info["icon"]; title_key = app_info["title_key"]

        if app_name in self.open_windows and self.open_windows[app_name]['window'].winfo_exists():
            win = self.open_windows[app_name]['window']; win.lift(); win.focus_force()
            try:
                if win.state() == 'iconic': win.deiconify()
            except tk.TclError: pass
        else:
            proc_user = self.sim_os.current_user; proc_cmd = app_name
            new_pid = self.sim_os._add_process(proc_cmd, proc_user)

            app_window = tk.Toplevel(self.root); app_window.wm_attributes("-topmost", True); app_window.transient(self.root)
            title_args = {'user': self.sim_os.current_user} if title_key == "terminal_title" else {}
            # --- Изменено: Используем ключ заголовка из app_info ---
            app_window.title(tr(title_key, **title_args))
            # --- Конец изменения ---

            app_icon_photo = self._load_icon(icon_path, cache=self.icon_cache)
            if app_icon_photo:
                try: app_window.iconphoto(False, app_icon_photo)
                except tk.TclError as e: print(f"Не удалось установить иконку для окна {app_name}: {e}")

            taskbar_button = self._create_or_update_taskbar_button(app_name)

            self.open_windows[app_name] = {'window': app_window, 'taskbar_button': taskbar_button, 'icon': self.taskbar_icon_cache.get(icon_path), 'pid': new_pid}
            app_window.protocol("WM_DELETE_WINDOW", lambda name=app_name, pid=new_pid: self.close_app_window(name, pid))

            pass_args = []
            # --- Изменено: Добавляем Snake ---
            if window_class in [FileExplorerWindow, TerminalWindow, TaskManagerWindow, TextEditorWindow, SnakeGameWindow]: pass_args = [self.sim_os]
            # --- Конец изменения ---
            elif window_class == SettingsWindow: pass_args = [self.sim_os, self]
            # Калькулятору аргументы не нужны
            if window_class != CalculatorWindow:
                 window_class(app_window, *pass_args)
            else:
                 window_class(app_window) # Запускаем калькулятор без доп. аргументов

            self.update_taskbar_app_icons()

    # --- Методы запуска ---
    def launch_snake_game(self):
        """Запускает игру Змейка."""
        self.launch_app("snake", self.sim_os)
    def launch_settings(self): self.launch_app("settings", self)
    def launch_explorer(self): self.launch_app("explorer", self.sim_os)
    def launch_calculator(self): self.launch_app("calculator")
    def launch_terminal(self): self.launch_app("terminal", self.sim_os)
    def launch_task_manager(self): self.launch_app("taskmanager", self.sim_os)
    def launch_editor(self): self.launch_app("editor", self.sim_os) # Добавлен запуск редактора

    def apply_background_color(self, color_code):
        if color_code:
            print(f"[Desktop] Применение цвета фона: {color_code}")
            self.sim_os.desktop_bg_color = color_code
            if not self._wallpaper_photo: self.desktop_canvas.config(bg=color_code)
            self.update_icon_text_backgrounds(color_code)

    def apply_wallpaper(self, image_path):
        if image_path and os.path.exists(image_path):
             print(f"[Desktop] Применение обоев: {image_path}")
             self.sim_os.desktop_wallpaper_path = image_path
             self._update_wallpaper()
             self.update_icon_text_backgrounds(self.sim_os.desktop_bg_color)
        else: print(f"[Desktop] Ошибка: Неверный путь к обоям: {image_path}")

    def update_icon_text_backgrounds(self, bg_color):
         pass # Фон под текстом иконок пока не используется


# --- ЗАМЕНИТЬ ЭТОТ КЛАСС ПОЛНОСТЬЮ ---

class FileExplorerWindow:
    """Окно Проводника (с копированием/вставкой, контекстным меню и сортировкой)."""
    def __init__(self, root, sim_os_instance):
        self.root = root
        self.sim_os = sim_os_instance
        self.root.title(tr("explorer_title"))
        self.root.geometry("650x450")
        self.root.minsize(500, 300)
        self.root.wm_attributes("-topmost", True)

        # --- Буфер обмена: action='copy'/'cut', source_path=путь, node_copy=скопированный узел (только для copy) ---
        self.clipboard = {'action': None, 'source_path': None, 'node_copy': None}

        # --- Верхняя панель ---
        top_frame = ttk.Frame(self.root, padding="5"); top_frame.pack(fill=tk.X)
        up_button = ttk.Button(top_frame, text=tr("up_button"), command=self.go_up, width=7); up_button.pack(side=tk.LEFT, padx=2)
        ttk.Label(top_frame, text=tr("path_label")).pack(side=tk.LEFT, padx=(10, 2))
        self.path_var = tk.StringVar(value=self.sim_os.get_cwd_string()); path_entry = ttk.Entry(top_frame, textvariable=self.path_var, state="readonly"); path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        button_frame = ttk.Frame(top_frame); button_frame.pack(side=tk.RIGHT)
        properties_button = ttk.Button(button_frame, text=tr("properties_button"), command=self.show_properties, width=9); properties_button.pack(side=tk.RIGHT, padx=2)
        rename_button = ttk.Button(button_frame, text=tr("rename_button"), command=self.rename_item, width=7); rename_button.pack(side=tk.RIGHT, padx=2)
        delete_button = ttk.Button(button_frame, text=tr("delete_button"), command=self.delete_item, width=8); delete_button.pack(side=tk.RIGHT, padx=2)
        touch_button = ttk.Button(button_frame, text=tr("file_button"), command=self.create_file, width=6); touch_button.pack(side=tk.RIGHT, padx=2)
        mkdir_button = ttk.Button(button_frame, text=tr("folder_button"), command=self.create_folder, width=6); mkdir_button.pack(side=tk.RIGHT, padx=2)
        refresh_button = ttk.Button(button_frame, text=tr("refresh_button"), command=self.refresh_view, width=5); refresh_button.pack(side=tk.RIGHT, padx=2)

        # --- Основная область (Дерево файлов) ---
        tree_frame = ttk.Frame(self.root); tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree = ttk.Treeview(tree_frame, columns=("type", "size", "owner", "permissions"), show="tree headings")
        self.tree.heading("#0", text=tr("tree_col_name"), command=lambda: self.sort_column("#0", False)); self.tree.heading("type", text=tr("tree_col_type"), command=lambda: self.sort_column("type", False))
        self.tree.heading("size", text=tr("tree_col_size"), command=lambda: self.sort_column("size", False)); self.tree.heading("owner", text=tr("tree_col_owner"), command=lambda: self.sort_column("owner", False))
        self.tree.heading("permissions", text=tr("tree_col_permissions"), command=lambda: self.sort_column("permissions", False))
        self.tree.column("#0", width=250, stretch=tk.YES); self.tree.column("type", width=60, anchor='center', stretch=tk.NO); self.tree.column("size", width=80, anchor='e', stretch=tk.NO)
        self.tree.column("owner", width=80, anchor='w', stretch=tk.NO); self.tree.column("permissions", width=90, anchor='center', stretch=tk.NO)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview); hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set); vsb.pack(side="right", fill="y"); hsb.pack(side="bottom", fill="x"); self.tree.pack(side="left", fill="both", expand=True)

        # --- Привязка событий ---
        self.tree.bind("<Double-1>", self.on_double_click); self.tree.bind("<Return>", self.on_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self._sort_column = "#0"; self._sort_reverse = False
        self.refresh_view()

        # --- Горячие клавиши ---
        self.root.bind("<F5>", lambda event: self.refresh_view()); self.root.bind("<Delete>", lambda event: self.delete_item())
        self.root.bind("<F2>", lambda event: self.rename_item()); self.root.bind("<Control-Shift-N>", lambda event: self.create_folder())
        self.root.bind("<Control-n>", lambda event: self.create_file()); self.root.bind("<BackSpace>", lambda event: self.go_up())
        # --- Добавлено: Ctrl+C, Ctrl+X, Ctrl+V ---
        self.root.bind("<Control-c>", lambda event: self.copy_item())
        self.root.bind("<Control-x>", lambda event: self.cut_item()) # Добавлено Cut
        self.root.bind("<Control-v>", lambda event: self.paste_item())
        # --- Конец добавления ---
        print("[Explorer] Локальные горячие клавиши привязаны.")

    # --- НОВЫЙ МЕТОД ---
    def copy_item(self):
        """Копирует выбранный элемент в буфер обмена."""
        selected_iids = self.tree.selection()
        if not selected_iids: return
        item_iid = selected_iids[0] # Копируем первый выбранный
        if item_iid == '/': messagebox.showwarning("Копирование", "Нельзя копировать корневой каталог.", parent=self.root); return
        try:
            node_copy, original_name = self.sim_os.do_copy_for_gui(item_iid)
            self.clipboard['node'] = node_copy
            self.clipboard['name'] = original_name
            self.clipboard['action'] = 'copy'
            self.clipboard['source_path'] = item_iid # Сохраняем исходный путь
            print(f"[Explorer] Скопировано в буфер (Copy): {original_name}")
        except Exception as e:
            messagebox.showerror(tr("error"), f"Не удалось скопировать:\n{e}", parent=self.root)
            self.clipboard = {'action': None, 'source_path': None, 'node_copy': None}

    # --- НОВЫЙ МЕТОД ---
    def cut_item(self):
        """Помещает выбранный элемент в буфер для вырезания."""
        selected_iids = self.tree.selection()
        if not selected_iids: return
        item_iid = selected_iids[0]
        if item_iid == '/': messagebox.showwarning("Вырезание", "Нельзя вырезать корневой каталог.", parent=self.root); return
        # Просто сохраняем путь и действие, сам узел не копируем
        self.clipboard['node'] = None # Очищаем узел, если там было что-то от copy
        self.clipboard['name'] = self.tree.item(item_iid, 'text') # Берем имя из дерева
        self.clipboard['action'] = 'cut'
        self.clipboard['source_path'] = item_iid
        print(f"[Explorer] Помещено в буфер (Cut): {self.clipboard['name']}")
        # Можно добавить визуальное отображение "вырезанного" элемента (например, серым цветом)
        # self.tree.item(item_iid, tags=('cut',))
        # self.tree.tag_configure('cut', foreground='grey')

    # --- НОВЫЙ МЕТОД ---
    def paste_item(self):
        """Вставляет элемент из буфера обмена в текущую директорию."""
        action = self.clipboard.get('action')
        if not action:
            messagebox.showwarning(tr("warning"), "Буфер обмена пуст.", parent=self.root)
            return

        current_dir = self.sim_os.get_cwd_string()
        source_path = self.clipboard['source_path']

        try:
            if action == 'copy':
                node_to_paste = copy.deepcopy(self.clipboard['node']) # Нужна копия для многократной вставки
                original_name = self.clipboard['name']
                if node_to_paste is None or original_name is None: raise ValueError("Данные для копирования повреждены.")
                self.sim_os.do_paste_for_gui(current_dir, node_to_paste, original_name)
            elif action == 'cut':
                if source_path is None: raise ValueError("Исходный путь для вырезания не найден.")
                # Проверяем, не пытаемся ли вставить в ту же папку или внутрь себя
                dest_dir_list = self.sim_os._resolve_path(current_dir)
                source_parent_list = self.sim_os._resolve_path(os.path.dirname(source_path).replace("\\","/"))
                if source_parent_list == dest_dir_list:
                     print("[Paste] Попытка вставить в ту же папку, где был вырезан элемент. Операция отменена.")
                     # Очищаем буфер, так как вырезание не состоялось
                     self.clipboard = {'action': None, 'source_path': None, 'node_copy': None}
                     return
                # Вызываем do_move_for_gui
                self.sim_os.do_move_for_gui(source_path, current_dir)
                # Очищаем буфер после успешного вырезания
                self.clipboard = {'action': None, 'source_path': None, 'node_copy': None}
            else:
                 raise ValueError("Неизвестное действие в буфере обмена.")

            self.refresh_view() # Обновляем вид
        except Exception as e:
            messagebox.showerror(tr("error"), f"Не удалось вставить:\n{e}", parent=self.root)
            # Не очищаем буфер при ошибке, чтобы пользователь мог попробовать вставить в другое место

    # --- Переработанный метод show_context_menu ---
    def show_context_menu(self, event):
        """Показывает контекстное меню для элемента Treeview или пустого места."""
        item_iid = self.tree.identify_row(event.y)
        context_menu = tk.Menu(self.root, tearoff=0)
        can_paste = self.clipboard.get('action') is not None

        if not item_iid: # Клик по пустому месту
            context_menu.add_command(label=tr("new_folder_title"), command=self.create_folder)
            context_menu.add_command(label=tr("new_file_title"), command=self.create_file)
            context_menu.add_command(label="Вставить", command=self.paste_item, state=tk.NORMAL if can_paste else tk.DISABLED) # TODO: Перевести
            context_menu.add_separator()
            context_menu.add_command(label=tr("refresh_button"), command=self.refresh_view)
        else:
            # Выделяем элемент
            if item_iid not in self.tree.selection():
                self.tree.selection_set(item_iid); self.tree.focus(item_iid)

            item_info = self.tree.item(item_iid)
            item_type = item_info['tags'][0] if item_info['tags'] else self.tree.set(item_iid, "type")
            is_root = (item_iid == '/')

            # --- Команды для элемента ---
            if item_type == 'folder': context_menu.add_command(label="Открыть", command=lambda iid=item_iid: self.open_folder(iid))
            elif item_type == 'file': context_menu.add_command(label="Открыть в редакторе", command=lambda iid=item_iid: self.open_in_editor(iid))
            context_menu.add_separator()
            context_menu.add_command(label="Копировать", command=self.copy_item, state=tk.DISABLED if is_root else tk.NORMAL) # TODO: Перевести
            context_menu.add_command(label="Вырезать", command=self.cut_item, state=tk.DISABLED if is_root else tk.NORMAL) # TODO: Перевести
            context_menu.add_command(label="Вставить", command=self.paste_item, state=tk.NORMAL if can_paste and item_type == 'folder' else tk.DISABLED) # Вставляем только в папки
            context_menu.add_separator()
            context_menu.add_command(label=tr("rename_button"), command=self.rename_item, state=tk.DISABLED if is_root else tk.NORMAL)
            context_menu.add_command(label=tr("delete_button"), command=self.delete_item, state=tk.DISABLED if is_root else tk.NORMAL)
            context_menu.add_separator()
            context_menu.add_command(label=tr("properties_button"), command=self.show_properties)

        try: context_menu.tk_popup(event.x_root, event.y_root)
        finally: context_menu.grab_release()

    # --- Методы open_folder, open_in_editor, sort_column, get_full_path, populate_tree ---
    # --- refresh_view, go_up, on_double_click, create_folder, create_file ---
    # --- delete_item, rename_item, show_properties, update_language ---
    # --- ОСТАЮТСЯ БЕЗ ИЗМЕНЕНИЙ (скопируйте их из предыдущей версии) ---
    def open_folder(self, folder_iid):
        try: self.sim_os.do_cd_for_gui(folder_iid); self.refresh_view()
        except Exception as e: messagebox.showerror(tr("error_nav"), str(e), parent=self.root)
    def open_in_editor(self, file_iid):
        desktop_window = None; parent = self.root.master
        while parent:
             if isinstance(parent, tk.Tk) and hasattr(parent, 'desktop_instance'): desktop_window = parent.desktop_instance; break
             parent = parent.master
        if desktop_window: desktop_window.launch_app("editor", self.sim_os, file_iid) # Передаем путь
        else: messagebox.showerror(tr("error"), "Не удалось найти главный рабочий стол для запуска редактора.", parent=self.root)
    def sort_column(self, col, reverse):
        try:
            if col == "#0": l = [(self.tree.item(k, 'text'), k) for k in self.tree.get_children('')]
            else: l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        except Exception as e: print(f"Ошибка при получении данных для сортировки колонки '{col}': {e}"); traceback.print_exc(); messagebox.showerror(tr("error_sort_title"), tr("error_sort_get", col=col), parent=self.root); return
        try:
            if col == "size": l.sort(key=lambda t: int(t[0]) if isinstance(t[0], str) and t[0].isdigit() else -1, reverse=reverse)
            else: l.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)
        except Exception as e: print(f"Ошибка при сравнении во время сортировки колонки '{col}': {e}"); l.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)
        for index, (val, k) in enumerate(l):
            try: self.tree.move(k, '', index)
            except tk.TclError: pass
            except Exception as e: print(f"Ошибка при перемещении элемента {k} во время сортировки: {e}")
        try: self.tree.heading(col, command=lambda: self.sort_column(col, not reverse)); self._sort_column = col; self._sort_reverse = reverse
        except Exception as e: print(f"Ошибка при обновлении заголовка колонки '{col}' после сортировки: {e}")
    def get_full_path(self, item_name):
        current_path = self.sim_os.get_cwd_string();
        if current_path == '/': return '/' + item_name if not item_name.startswith('/') else item_name
        else: return os.path.join(current_path, item_name).replace("\\", "/")
    def populate_tree(self, path):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            content = self.sim_os.do_ls_for_gui(path)
            for item in content:
                name = item['name']; display_name = item.get('display_name', name); item_type = item['type']; item_size = item['size']
                owner = item.get('owner', '?'); perms = item.get('permissions', '---------')
                full_item_path = self.get_full_path(name)
                self.tree.insert('', 'end', iid=full_item_path, text=display_name, values=(item_type, item_size, owner, perms), tags=(item_type,))
            self.tree.tag_configure('folder', foreground='blue'); self.tree.tag_configure('link', foreground='cyan')
            if self._sort_column: self.sort_column(self._sort_column, self._sort_reverse)
        except Exception as e: messagebox.showerror(tr("error"), tr("error_read_dir") + f":\n{e}", parent=self.root); traceback.print_exc()
    def refresh_view(self): current_path = self.sim_os.get_cwd_string(); self.path_var.set(current_path); self.populate_tree(current_path)
    def go_up(self):
        """Переходит на уровень вверх."""
        current_path = self.sim_os.get_cwd_string()
        if current_path == '/':
            return # Некуда идти вверх из корня
        try:
            # Получаем путь к родительской директории
            parent_path = os.path.dirname(current_path).replace("\\", "/")
            # dirname от /file вернет '', нужно обработать это как корень '/'
            # Проверяем, что parent_path не пустой И что текущий путь не был корнем
            # (чтобы избежать бесконечного цикла, если dirname вернул '' для '/')
            if not parent_path and current_path != '/':
                 parent_path = '/'

            # Вызываем cd и refresh только если путь корректный
            self.sim_os.do_cd_for_gui(parent_path)
            self.refresh_view()
        except Exception as e:
            messagebox.showerror(tr("error_nav"), str(e), parent=self.root)


    def on_double_click(self, event=None):
        item_iid = self.tree.focus();
        if not item_iid: return
        item_info = self.tree.item(item_iid); item_type = item_info['tags'][0] if item_info['tags'] else self.tree.set(item_iid, "type")
        if item_type == 'folder': self.open_folder(item_iid)
        elif item_type == 'file': self.open_in_editor(item_iid)
    def create_folder(self):
        folder_name = simpledialog.askstring(tr("new_folder_title"), tr("new_folder_prompt"), parent=self.root)
        if folder_name:
            if '/' in folder_name or '\\' in folder_name: messagebox.showwarning(tr("warn_invalid_name"), tr("warn_invalid_name_folder"), parent=self.root); return
            try: full_path = self.get_full_path(folder_name); self.sim_os.do_mkdir_for_gui(full_path); self.refresh_view()
            except Exception as e: messagebox.showerror(tr("error_create_folder"), str(e), parent=self.root)
    def create_file(self):
        file_name = simpledialog.askstring(tr("new_file_title"), tr("new_file_prompt"), parent=self.root)
        if file_name:
            if '/' in file_name or '\\' in file_name: messagebox.showwarning(tr("warn_invalid_name"), tr("warn_invalid_name_file"), parent=self.root); return
            try: full_path = self.get_full_path(file_name); self.sim_os.do_touch_for_gui(full_path); self.refresh_view()
            except Exception as e: messagebox.showerror(tr("error_create_file"), str(e), parent=self.root)
    def delete_item(self):
        selected_iids = self.tree.selection();
        if not selected_iids: messagebox.showwarning(tr("delete_button"), tr("delete_warn_select"), parent=self.root); return
        items_to_delete_str = "\n".join([self.tree.item(iid)['text'] for iid in selected_iids])
        if messagebox.askyesno(tr("delete_title"), tr("delete_prompt", items=items_to_delete_str), icon='warning', parent=self.root):
            success_count = 0; error_count = 0
            for item_iid in selected_iids:
                try: self.sim_os.do_rm_for_gui(item_iid); success_count += 1
                except Exception as e: error_count += 1; messagebox.showerror(tr("error_delete"), f"Не удалось удалить '{self.tree.item(item_iid)['text']}':\n{e}", parent=self.root)
            if error_count > 0: messagebox.showwarning(tr("delete_button"), tr("delete_warn_errors", success=success_count, errors=error_count), parent=self.root)
            self.refresh_view()
    def rename_item(self):
        selected_iids = self.tree.selection()
        if not selected_iids: messagebox.showwarning(tr("rename_button"), tr("delete_warn_select"), parent=self.root); return
        if len(selected_iids) > 1: messagebox.showwarning(tr("rename_button"), tr("delete_warn_multi"), parent=self.root); return
        item_iid = selected_iids[0]; old_name = self.tree.item(item_iid, 'text')
        new_name = simpledialog.askstring(tr("rename_title"), tr("rename_prompt", old_name=old_name), initialvalue=old_name, parent=self.root)
        if new_name and new_name != old_name:
            try: self.sim_os.do_rename_for_gui(item_iid, new_name); self.refresh_view()
            except Exception as e: messagebox.showerror(tr("error_rename"), str(e), parent=self.root)
        elif new_name is None: pass
        elif new_name == old_name: pass
    def show_properties(self):
        selected_iids = self.tree.selection()
        if not selected_iids: messagebox.showwarning(tr("properties_button"), tr("delete_warn_select"), parent=self.root); return
        if len(selected_iids) > 1: messagebox.showwarning(tr("properties_button"), tr("delete_warn_multi"), parent=self.root); return
        item_iid = selected_iids[0]; item_info = self.tree.item(item_iid)
        try:
            resolved_path = self.sim_os._resolve_path(item_iid); node = self.sim_os._get_node_from_path(resolved_path)
            if node is None or 'meta' not in node: raise ValueError(tr("error_props_get"))
            meta = node['meta']; node_type = "folder" if 'children' in node else "file"
            content = node.get('content', '') if node_type == 'file' else None
            size_bytes = len(content.encode('utf-8')) if content is not None else meta.get('dir_size', 0)
            mtime_ts = meta.get('mtime', 0); mtime_str = datetime.datetime.fromtimestamp(mtime_ts).strftime('%Y-%m-%d %H:%M:%S') if mtime_ts else "N/A"
            ctime_ts = meta.get('ctime', 0); ctime_str = datetime.datetime.fromtimestamp(ctime_ts).strftime('%Y-%m-%d %H:%M:%S') if ctime_ts else "N/A"
        except Exception as e: messagebox.showerror(tr("error_props"), tr("error_props_get") + f":\n{e}", parent=self.root); traceback.print_exc(); return
        prop_win = tk.Toplevel(self.root); prop_win.wm_attributes("-topmost", True)
        prop_win.title(tr("properties_title", name=item_info['text'])); prop_win.geometry("350x280"); prop_win.resizable(False, False); prop_win.transient(self.root)
        frame = ttk.Frame(prop_win, padding="10"); frame.pack(fill=tk.BOTH, expand=True)
        row_idx = 0
        ttk.Label(frame, text=tr("properties_name")).grid(row=row_idx, column=0, sticky="w", pady=1); ttk.Label(frame, text=item_info['text']).grid(row=row_idx, column=1, sticky="w", pady=1); row_idx+=1
        ttk.Label(frame, text=tr("properties_type")).grid(row=row_idx, column=0, sticky="w", pady=1); ttk.Label(frame, text=node_type).grid(row=row_idx, column=1, sticky="w", pady=1); row_idx+=1
        ttk.Label(frame, text=tr("properties_size")).grid(row=row_idx, column=0, sticky="w", pady=1); ttk.Label(frame, text=tr("properties_size_bytes", size=size_bytes)).grid(row=row_idx, column=1, sticky="w", pady=1); row_idx+=1
        ttk.Label(frame, text=tr("properties_path")).grid(row=row_idx, column=0, sticky="w", pady=1); path_label = ttk.Label(frame, text=item_iid, wraplength=250); path_label.grid(row=row_idx, column=1, sticky="w", pady=1); row_idx+=1
        ttk.Label(frame, text=tr("properties_owner")).grid(row=row_idx, column=0, sticky="w", pady=1); ttk.Label(frame, text=meta.get('owner', '?')).grid(row=row_idx, column=1, sticky="w", pady=1); row_idx+=1
        ttk.Label(frame, text=tr("properties_permissions")).grid(row=row_idx, column=0, sticky="w", pady=1); ttk.Label(frame, text=meta.get('permissions', '---------')).grid(row=row_idx, column=1, sticky="w", pady=1); row_idx+=1
        ttk.Label(frame, text=tr("properties_mtime")).grid(row=row_idx, column=0, sticky="w", pady=1); ttk.Label(frame, text=mtime_str).grid(row=row_idx, column=1, sticky="w", pady=1); row_idx+=1
        ttk.Label(frame, text="Создан:").grid(row=row_idx, column=0, sticky="w", pady=1); ttk.Label(frame, text=ctime_str).grid(row=row_idx, column=1, sticky="w", pady=1); row_idx+=1
        ttk.Separator(frame, orient='horizontal').grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=8); row_idx+=1
        ok_button = ttk.Button(frame, text=tr("ok"), command=prop_win.destroy); ok_button.grid(row=row_idx, column=1, sticky='e'); ok_button.focus_set(); row_idx+=1
        prop_win.bind("<Return>", lambda e: prop_win.destroy()); frame.grid_columnconfigure(1, weight=1)
    def update_language(self):
        self.root.title(tr("explorer_title"))
        # TODO: Обновить тексты кнопок, меток, заголовков колонок
        print("[Explorer] update_language called (stub - needs implementation)")



class CalculatorWindow:
    """Окно простого калькулятора (без изменений)."""
    def __init__(self, root):
        self.root = root; self.root.wm_attributes("-topmost", True); self.root.title("Калькулятор"); self.root.geometry("300x350"); self.root.resizable(False, False)
        self.expression = ""; self.display_var = tk.StringVar()
        style = ttk.Style(); style.configure('Calc.TEntry', font=('Arial', 20))
        display = ttk.Entry(self.root, textvariable=self.display_var, style='Calc.TEntry', justify='right', state='readonly')
        display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        buttons = [('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
                   ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
                   ('C', 5, 0, 2), ('←', 5, 2, 2)]
        for i in range(4): self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(0, weight=0);
        for i in range(1, 6): self.root.grid_rowconfigure(i, weight=1)
        style.configure('Calc.TButton', font=('Arial', 14))
        for (text, row, col, *span) in buttons:
            colspan = span[0] if span else 1; action = lambda x=text: self.on_button_click(x)
            button = ttk.Button(self.root, text=text, style='Calc.TButton', command=action)
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)
        self.root.bind('<Key>', self.on_key_press); self.root.focus_set()
    def on_key_press(self, event):
        key = event.keysym; char = event.char
        if char.isdigit() or char == '.': self.on_button_click(char)
        elif char in "+-*/": self.on_button_click(char)
        elif key == 'Return' or key == 'equal': self.on_button_click('=')
        elif key == 'BackSpace': self.on_button_click('←')
        elif key == 'Escape' or (key == 'c' and not event.state & 0x4): self.on_button_click('C')
        elif char == '%': self.on_button_click('%')
    def on_button_click(self, char):
        current_text = self.expression
        if char == 'C': self.expression = ""
        elif char == '←': self.expression = current_text[:-1]
        elif char == '=':
            if not current_text: return
            try:
                safe_expression = re.sub(r"[^0-9+\-*/.%()\s]", "", current_text).replace('%', '/100.0')
                result = str(eval(safe_expression));
                if result.endswith('.0'): result = result[:-2]
                self.expression = result
            except ZeroDivisionError: self.expression = "Ошибка: /0"
            except Exception as e: print(f"Calc Error: {e}"); self.expression = "Ошибка"
        else:
            if char in "+-*/." and (not current_text or current_text[-1] in "+-*/."):
                 if char == '.' and current_text and current_text[-1].isdigit(): self.expression += str(char)
                 elif char != '.':
                      if current_text and current_text[-1] not in "+-*/.": self.expression += str(char)
                      elif not current_text and char == '-': self.expression += str(char)
            elif char == '.' and '.' in current_text.split()[-1]: pass
            else: self.expression += str(char)
        self.display_var.set(self.expression if self.expression else "0")


class TerminalWindow(tk.Toplevel):
    """Окно Терминала."""
    def __init__(self, root, sim_os_instance):
        super().__init__(root)
        self.wm_attributes("-topmost", True)
        self.root = root
        self.sim_os = sim_os_instance
        self.title(f"Терминал - {self.sim_os.current_user}")
        self.geometry("700x500")
        self.configure(bg="black") # Черный фон

        # Текстовое поле для вывода
        self.output_area = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, bg="black", fg="lightgrey",
            font=("Consolas", 10), # Моноширинный шрифт
            insertbackground="white", # Цвет курсора
            selectbackground="grey", # Цвет выделения
            state=tk.DISABLED # Начинаем в режиме только для чтения
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Поле для ввода команды
        self.input_frame = tk.Frame(self, bg="black")
        self.input_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.prompt_label = tk.Label(self.input_frame, text="", bg="black", fg="lightblue", font=("Consolas", 10))
        self.prompt_label.pack(side=tk.LEFT)

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            self.input_frame, textvariable=self.input_var,
            bg="black", fg="white", font=("Consolas", 10),
            insertbackground="white", relief=tk.FLAT # Убираем рамку
        )
        self.input_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self.input_entry.bind("<Return>", self.process_command)
        self.input_entry.focus_set()

        # История команд
        self.history = []
        self.history_index = -1
        self.input_entry.bind("<Up>", self.history_up)
        self.input_entry.bind("<Down>", self.history_down)

        # Отображаем первое приглашение
        self.show_prompt()

    def show_prompt(self):
        """Отображает приглашение командной строки."""
        user = self.sim_os.current_user
        cwd = self.sim_os.get_cwd_string()
        prompt_char = '#' if user == 'root' else '$'
        prompt_text = f"{user}@{self.sim_os.os_name.split()[0].lower()}:{cwd}{prompt_char} "
        self.prompt_label.config(text=prompt_text)

    def write_output(self, text, tag=None):
        """Записывает текст в область вывода."""
        self.output_area.config(state=tk.NORMAL)
        if tag:
            self.output_area.insert(tk.END, text, tag)
        else:
            self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END) # Прокрутить вниз
        self.output_area.config(state=tk.DISABLED)

    def process_command(self, event=None):
        """Обрабатывает введенную команду."""
        command = self.input_var.get()
        self.input_var.set("") # Очистить поле ввода

        # Отображаем введенную команду с приглашением
        prompt_text = self.prompt_label.cget("text")
        self.write_output(prompt_text + command + "\n")

        if command.strip():
            # Добавляем в историю только непустые команды
            if not self.history or self.history[-1] != command:
                 self.history.append(command)
            self.history_index = len(self.history) # Сброс индекса истории

            # Выполняем команду через SimOS
            stdout_val, stderr_val, exit_code = self.sim_os.execute_text_command(command)

            # Обработка специальных кодов возврата
            if exit_code == 0 and command.strip().lower() == 'clear':
                 self.output_area.config(state=tk.NORMAL)
                 self.output_area.delete('1.0', tk.END)
                 self.output_area.config(state=tk.DISABLED)
            elif exit_code == -1 and command.strip().lower() == 'exit':
                 self.destroy() # Закрыть окно терминала
                 return # Не показывать следующее приглашение
            else:
                 # Выводим stdout и stderr
                 if stdout_val:
                     self.write_output(stdout_val)
                 if stderr_val:
                     # Используем тег для выделения ошибок красным
                     self.output_area.tag_configure("error", foreground="red")
                     self.write_output(stderr_val, "error")

        # Показываем следующее приглашение
        self.show_prompt()

    def history_up(self, event=None):
        """Перемещается вверх по истории команд."""
        if self.history:
            if self.history_index > 0:
                self.history_index -= 1
            elif self.history_index == -1: # Если еще не в истории
                 self.history_index = len(self.history) - 1

            if self.history_index >= 0:
                 self.input_var.set(self.history[self.history_index])
                 self.input_entry.icursor(tk.END) # Переместить курсор в конец
        return "break" # Предотвратить стандартную обработку Up

    def history_down(self, event=None):
        """Перемещается вниз по истории команд."""
        if self.history:
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.input_var.set(self.history[self.history_index])
            else: # Дошли до конца истории
                 self.history_index = len(self.history)
                 self.input_var.set("") # Очистить поле ввода
            self.input_entry.icursor(tk.END)
        return "break"


class SettingsWindow(tk.Toplevel):
    """Окно Настроек SimOS."""
    def __init__(self, root, sim_os_instance, desktop_window_instance):
        super().__init__(root)
        self.root = root # Это Toplevel окно
        self.sim_os = sim_os_instance
        self.desktop_window = desktop_window_instance # Ссылка на DesktopWindow

        self.title(tr("settings_title"))
        self.geometry("450x350") # Немного увеличим
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.transient(root.master) # Связываем с главным окном (root.master)

        # --- Основной фрейм ---
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Информация о системе ---
        info_frame = ttk.LabelFrame(main_frame, text=tr("os_info_label"), padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(info_frame, text=tr("os_version_label")).grid(row=0, column=0, sticky="w")
        ttk.Label(info_frame, text=self.sim_os.os_name).grid(row=0, column=1, sticky="w", padx=5)

        # --- Настройки внешнего вида ---
        appearance_frame = ttk.LabelFrame(main_frame, text=tr("appearance_label"), padding="10")
        appearance_frame.pack(fill=tk.X, pady=(0, 10))

        # -- Цвет фона (фоллбэк) --
        ttk.Label(appearance_frame, text=tr("desktop_bg_label")).grid(row=0, column=0, sticky="w", pady=5, padx=(0,5))
        self.current_color_label = tk.Label(appearance_frame, text=self.sim_os.desktop_bg_color,
                                            bg=self.sim_os.desktop_bg_color, width=10, relief=tk.SUNKEN, borderwidth=1)
        self.update_color_label_text_color()
        self.current_color_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        color_button = ttk.Button(appearance_frame, text=tr("choose_color_button"), command=self.choose_color)
        color_button.grid(row=0, column=2, columnspan=2, sticky="w", padx=5, pady=5) # Объединяем колонки для кнопки

        # -- Обои рабочего стола --
        ttk.Label(appearance_frame, text=tr("wallpaper_label")).grid(row=1, column=0, sticky="w", pady=5, padx=(0,5))
        self.wallpaper_path_var = tk.StringVar(value=self.sim_os.desktop_wallpaper_path)
        wallpaper_entry = ttk.Entry(appearance_frame, textvariable=self.wallpaper_path_var, state="readonly", width=30)
        wallpaper_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5) # Растягиваем поле
        browse_button = ttk.Button(appearance_frame, text=tr("browse_button"), command=self.browse_wallpaper)
        browse_button.grid(row=1, column=3, sticky="w", padx=5, pady=5) # Кнопка справа

        appearance_frame.grid_columnconfigure(1, weight=1) # Растягиваем колонку с цветом/путем

        # --- Кнопка Закрыть ---
        close_button = ttk.Button(main_frame, text=tr("ok"), command=self.destroy)
        close_button.pack(side=tk.BOTTOM, pady=(15, 0))
        close_button.focus_set()
        self.bind("<Return>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.destroy())

    def choose_color(self):
        """Открывает диалог выбора цвета и применяет его."""
        color_info = colorchooser.askcolor(title=tr("choose_bg_color"),
                                           initialcolor=self.sim_os.desktop_bg_color, parent=self)
        if color_info and color_info[1]:
            new_color_hex = color_info[1]
            self.desktop_window.apply_background_color(new_color_hex)
            self.current_color_label.config(text=new_color_hex, bg=new_color_hex)
            self.update_color_label_text_color()

    def browse_wallpaper(self):
        """Открывает диалог выбора файла обоев."""
        filetypes = [ (tr("image_files"), "*.png *.jpg *.jpeg *.bmp *.gif"), (tr("all_files"), "*.*") ]
        initial_dir = os.path.dirname(self.sim_os.desktop_wallpaper_path)
        if not os.path.isdir(initial_dir): initial_dir = os.path.abspath(os.path.expanduser("~"))

        filepath = filedialog.askopenfilename(title=tr("select_wallpaper_title"),
                                              initialdir=initial_dir,
                                              filetypes=filetypes, parent=self)
        if filepath:
            self.desktop_window.apply_wallpaper(filepath)
            self.wallpaper_path_var.set(filepath)

    def update_color_label_text_color(self):
         """Устанавливает цвет текста (черный/белый) для метки с цветом фона."""
         bg_color = self.current_color_label.cget('bg')
         try:
             rgb = self.winfo_rgb(bg_color)
             brightness = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 65535
             text_color = "black" if brightness > 0.5 else "white"
             self.current_color_label.config(fg=text_color)
         except tk.TclError: self.current_color_label.config(fg="black")

    def update_language(self):
        """Обновляет тексты в окне Настроек."""
        self.title(tr("settings_title"))
        # TODO: Обновить тексты всех Label, Button, LabelFrame
        print("[SettingsWindow] update_language called (stub - needs full implementation)")


class TaskManagerWindow(tk.Toplevel):
    """Окно Диспетчера задач SimOS (с сортировкой)."""
    REFRESH_INTERVAL = 2000

    def __init__(self, root, sim_os_instance):
        super().__init__(root)
        self.root = root
        self.sim_os = sim_os_instance
        self._after_id = None
        self._sort_column = "pid" # Колонка сортировки по умолчанию
        self._sort_reverse = False

        self.title(tr("taskmgr_title"))
        self.geometry("600x450")
        self.minsize(450, 300)
        self.wm_attributes("-topmost", True)
        self.transient(root.master)

        # --- Ресурсы ---
        resource_frame = ttk.Frame(self, padding="10"); resource_frame.pack(fill=tk.X)
        self.cpu_label = ttk.Label(resource_frame, text=tr("taskmgr_cpu_label", cores=self.sim_os.total_cores))
        self.cpu_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.cpu_progress = ttk.Progressbar(resource_frame, orient='horizontal', length=100, mode='determinate', maximum=100 * self.sim_os.total_cores)
        self.cpu_progress.grid(row=0, column=1, sticky="ew", pady=2)
        self.cpu_value_label = ttk.Label(resource_frame, text="0.0%", width=7, anchor="e")
        self.cpu_value_label.grid(row=0, column=2, sticky="e", padx=(5, 0))
        self.ram_label = ttk.Label(resource_frame, text=tr("taskmgr_ram_label"))
        self.ram_label.grid(row=1, column=0, sticky="w", padx=(0, 5))
        self.ram_progress = ttk.Progressbar(resource_frame, orient='horizontal', length=100, mode='determinate', maximum=self.sim_os.total_ram_mb)
        self.ram_progress.grid(row=1, column=1, sticky="ew", pady=2)
        self.ram_value_label = ttk.Label(resource_frame, text=tr("taskmgr_ram_usage", used=0.0, total=self.sim_os.total_ram_mb), width=20, anchor="e")
        self.ram_value_label.grid(row=1, column=2, sticky="e", padx=(5, 0))
        resource_frame.grid_columnconfigure(1, weight=1)

        # --- Процессы ---
        process_frame = ttk.LabelFrame(self, text=tr("taskmgr_processes_label"), padding="10")
        process_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 0))
        cols = ("pid", "user", "cpu", "ram", "command")
        self.tree = ttk.Treeview(process_frame, columns=cols, show="headings")
        # --- Изменено: Добавлены команды сортировки ---
        self.tree.heading("pid", text=tr("taskmgr_pid_col"), command=lambda: self.sort_column("pid", False))
        self.tree.heading("user", text=tr("taskmgr_user_col"), command=lambda: self.sort_column("user", False))
        self.tree.heading("cpu", text=tr("taskmgr_cpu_col"), command=lambda: self.sort_column("cpu", False))
        self.tree.heading("ram", text=tr("taskmgr_ram_col"), command=lambda: self.sort_column("ram", False))
        self.tree.heading("command", text=tr("taskmgr_command_col"), command=lambda: self.sort_column("command", False))
        # --- Конец изменений ---
        self.tree.column("pid", width=50, anchor="e", stretch=tk.NO); self.tree.column("user", width=80, stretch=tk.NO)
        self.tree.column("cpu", width=60, anchor="e", stretch=tk.NO); self.tree.column("ram", width=90, anchor="e", stretch=tk.NO)
        self.tree.column("command", width=200, stretch=tk.YES)
        vsb = ttk.Scrollbar(process_frame, orient="vertical", command=self.tree.yview); hsb = ttk.Scrollbar(process_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set); vsb.pack(side="right", fill="y"); hsb.pack(side="bottom", fill="x"); self.tree.pack(side="left", fill="both", expand=True)

        # --- Низ ---
        bottom_frame = ttk.Frame(self, padding=(10, 5, 10, 10)); bottom_frame.pack(fill=tk.X)
        self.kill_button = ttk.Button(bottom_frame, text=tr("taskmgr_kill_button"), command=self.kill_selected_process, state=tk.DISABLED)
        self.kill_button.pack(side=tk.RIGHT)
        self.tree.bind("<<TreeviewSelect>>", self.on_process_select)
        self.update_display() # Первое обновление
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # --- НОВЫЙ МЕТОД ---
    def sort_column(self, col, reverse):
        """Сортирует процессы по выбранной колонке."""
        try:
            # Получаем данные из Treeview в виде списка кортежей (значение_колонки, iid)
            l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        except Exception as e:
            print(f"Ошибка получения данных для сортировки колонки '{col}': {e}"); return

        # Определяем ключ сортировки
        sort_key = None
        if col in ["pid", "cpu", "ram"]: # Числовые колонки
            sort_key = lambda t: float(t[0]) if isinstance(t[0], str) and re.match(r"^-?\d+(\.\d+)?$", t[0]) else -1.0
        else: # Строковые колонки (user, command)
            sort_key = lambda t: str(t[0]).lower()

        try:
            l.sort(key=sort_key, reverse=reverse)
        except Exception as e:
            print(f"Ошибка при сортировке колонки '{col}': {e}")
            # Фоллбэк на простую строковую сортировку
            l.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)

        # Перемещаем элементы
        for index, (val, k) in enumerate(l):
            try: self.tree.move(k, '', index)
            except tk.TclError: pass # Элемент мог быть удален во время сортировки

        # Обновляем команду для заголовка (для смены направления)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
        self._sort_column = col
        self._sort_reverse = reverse

    def on_close(self):
        if self._after_id: self.after_cancel(self._after_id); self._after_id = None; print("[TaskManager] Refresh timer stopped.")
        self.destroy()

    def on_process_select(self, event=None):
        self.kill_button.config(state=tk.NORMAL if self.tree.selection() else tk.DISABLED)

    # --- Переработанный метод update_display ---
    def update_display(self):
        """Обновляет информацию о ресурсах и процессах."""
        # --- Обновляем ресурсы ---
        try:
            summary = self.sim_os.get_resource_summary()
            cpu_perc = summary['total_cpu_percent']; ram_used = summary['total_ram_used_mb']; ram_total = summary['total_ram_mb']
            self.cpu_progress['maximum'] = 100 * summary['total_cores']; self.cpu_progress['value'] = cpu_perc
            self.cpu_value_label.config(text=f"{cpu_perc:.1f}%")
            self.ram_progress['maximum'] = ram_total; self.ram_progress['value'] = ram_used
            self.ram_value_label.config(text=tr("taskmgr_ram_usage", used=ram_used, total=ram_total))
            self.cpu_label.config(text=tr("taskmgr_cpu_label", cores=summary['total_cores']))
        except Exception as e: print(f"Ошибка обновления ресурсов: {e}")

        # --- Обновляем список процессов ---
        try:
            processes = self.sim_os.get_process_list()
            selected_item = self.tree.selection()
            # --- Используем словарь для быстрого доступа к существующим элементам ---
            current_items = {self.tree.set(item_id, "pid"): item_id for item_id in self.tree.get_children()}
            new_pids = {str(p['pid']) for p in processes}

            # Удаляем процессы
            for pid_str, item_id in list(current_items.items()):
                if pid_str not in new_pids:
                    if self.tree.exists(item_id): self.tree.delete(item_id)
                    del current_items[pid_str]

            # Обновляем/добавляем процессы
            for proc in processes:
                pid_str = str(proc.get('pid', '?'))
                values = ( proc.get('pid', '?'), proc.get('user', '?'),
                           f"{proc.get('cpu', 0.0):.1f}", f"{proc.get('ram', 0.0):.1f}",
                           proc.get('command', '?') )
                if pid_str in current_items:
                    self.tree.item(current_items[pid_str], values=values)
                else:
                    new_item_id = self.tree.insert('', 'end', iid=pid_str, values=values)
                    current_items[pid_str] = new_item_id # Добавляем в словарь

            # --- Применяем сортировку после обновления ---
            if self._sort_column:
                 self.sort_column(self._sort_column, self._sort_reverse)

            # Восстанавливаем выделение
            if selected_item and self.tree.exists(selected_item[0]):
                 self.tree.selection_set(selected_item[0]); self.tree.focus(selected_item[0])
            else: self.tree.selection_set()

        except Exception as e: print(f"Ошибка обновления списка процессов: {e}"); traceback.print_exc()

        self.on_process_select() # Обновляем состояние кнопки
        if self.winfo_exists(): self._after_id = self.after(self.REFRESH_INTERVAL, self.update_display)

    def kill_selected_process(self):
        """Завершает выбранный процесс."""
        selected_items = self.tree.selection()
        if not selected_items: return
        item_iid = selected_items[0]
        try:
            pid_to_kill = int(item_iid); command = self.tree.set(item_iid, "command")
            if messagebox.askyesno(tr("taskmgr_kill_confirm_title"), tr("taskmgr_kill_confirm_msg", pid=pid_to_kill, command=command), icon='warning', parent=self):
                try:
                    self.sim_os.kill_process(pid_to_kill)
                    if self.tree.exists(item_iid): self.tree.delete(item_iid) # Удаляем сразу
                    # Обновляем ресурсы сразу
                    summary = self.sim_os.get_resource_summary(); cpu_perc = summary['total_cpu_percent']; ram_used = summary['total_ram_used_mb']; ram_total = summary['total_ram_mb']
                    self.cpu_progress['value'] = cpu_perc; self.cpu_value_label.config(text=f"{cpu_perc:.1f}%")
                    self.ram_progress['value'] = ram_used; self.ram_value_label.config(text=tr("taskmgr_ram_usage", used=ram_used, total=ram_total))
                except (ValueError, PermissionError, OSError) as kill_e: messagebox.showerror(tr("taskmgr_kill_error_title"), str(kill_e), parent=self)
                except Exception as kill_e: messagebox.showerror(tr("taskmgr_kill_error_title"), f"Неизвестная ошибка: {kill_e}", parent=self); traceback.print_exc()
        except ValueError: messagebox.showerror(tr("taskmgr_kill_error_title"), "Неверный PID выбранного процесса.", parent=self)
        except Exception as e: messagebox.showerror(tr("taskmgr_kill_error_title"), f"Ошибка при попытке завершения: {e}", parent=self); traceback.print_exc()

    def update_language(self):
        """Обновляет язык в Диспетчере задач."""
        self.title(tr("taskmgr_title"))
        self.cpu_label.config(text=tr("taskmgr_cpu_label", cores=self.sim_os.total_cores))
        self.ram_label.config(text=tr("taskmgr_ram_label"))
        try: summary = self.sim_os.get_resource_summary(); self.ram_value_label.config(text=tr("taskmgr_ram_usage", used=summary['total_ram_used_mb'], total=summary['total_ram_mb']))
        except: pass
        # Обновляем заголовок фрейма процессов
        # Нужно сохранить ссылку на process_frame в self.__init__ или найти его
        try: self.winfo_children()[1].config(text=tr("taskmgr_processes_label")) # Предполагаем, что это второй виджет
        except: pass
        self.kill_button.config(text=tr("taskmgr_kill_button"))
        self.tree.heading("pid", text=tr("taskmgr_pid_col")); self.tree.heading("user", text=tr("taskmgr_user_col"))
        self.tree.heading("cpu", text=tr("taskmgr_cpu_col")); self.tree.heading("ram", text=tr("taskmgr_ram_col"))
        self.tree.heading("command", text=tr("taskmgr_command_col"))
        # Обновляем данные, чтобы применить форматирование, если оно зависит от локали
        # self.update_display() # Не вызываем здесь, чтобы не сбить таймер
        print("[TaskManager] update_language called")


class TextEditorWindow(tk.Toplevel):
    """Окно простого текстового редактора."""
    def __init__(self, root, sim_os_instance, file_path=None):
        super().__init__(root)
        self.root_parent = root # Сохраняем ссылку на родителя Toplevel
        self.sim_os = sim_os_instance
        self.current_file_path = None # Начинаем без файла
        self.text_modified = False

        self.title(tr("editor_untitled") + " - " + tr("editor_title"))
        self.geometry("600x500")
        self.minsize(300, 200)
        self.wm_attributes("-topmost", True)
        self.transient(root.master)

        # --- Меню редактора ---
        menubar = tk.Menu(self); self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0); menubar.add_cascade(label=tr("editor_menu_file"), menu=file_menu)
        file_menu.add_command(label=tr("editor_menu_new"), command=self.new_file); file_menu.add_command(label=tr("editor_menu_open"), command=self.open_file)
        file_menu.add_command(label=tr("editor_menu_save"), command=self.save_file); file_menu.add_command(label=tr("editor_menu_save_as"), command=self.save_file_as)
        file_menu.add_separator(); file_menu.add_command(label=tr("editor_menu_exit"), command=self.close_window)

        # --- Текстовое поле ---
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, undo=True, font=("Consolas", 10))
        self.text_area.pack(fill=tk.BOTH, expand=True); self.text_area.focus_set()
        self.text_area.bind("<<Modified>>", self.on_text_change)

        # Загрузка файла, если путь был передан при создании окна
        if file_path: self.load_file_content(file_path)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def on_text_change(self, event=None):
        try:
             if self.text_area.edit_modified(): self.text_modified = True; self.update_title()
             self.text_area.edit_modified(False)
        except tk.TclError: pass

    def update_title(self):
        base_name = os.path.basename(self.current_file_path) if self.current_file_path else tr("editor_untitled")
        modified_marker = "*" if self.text_modified else ""
        self.title(f"{modified_marker}{base_name} - {tr('editor_title')}")

    def new_file(self):
        if not self.check_save_before_close(): return
        self.text_area.delete('1.0', tk.END); self.current_file_path = None
        self.text_modified = False; self.text_area.edit_modified(False); self.update_title()

    def open_file(self):
        """Открывает файл для редактирования (запрашивает путь)."""
        if not self.check_save_before_close(): return
        # Запрашиваем путь внутри SimOS
        filepath = simpledialog.askstring(tr("editor_open_title"),
                                          "Введите полный путь к файлу в SimOS:",
                                          parent=self)
        if filepath:
            self.load_file_content(filepath)

    def load_file_content(self, filepath):
        """Загружает содержимое файла из SimOS."""
        try:
            # Проверяем, существует ли файл перед чтением
            resolved = self.sim_os._resolve_path(filepath)
            node = self.sim_os._get_node_from_path(resolved) if resolved else None
            if node is None or 'content' not in node:
                 raise FileNotFoundError(f"Файл не найден или не является файлом: {filepath}")

            content = self.sim_os.read_file_for_gui(filepath) # Проверка прав внутри
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', content)
            self.current_file_path = filepath
            self.text_modified = False
            self.text_area.edit_modified(False)
            self.update_title()
        except Exception as e:
            messagebox.showerror(tr("error"), tr("error_read_file") + f":\n{e}", parent=self)

    def save_file(self):
        """Сохраняет текущий файл."""
        if not self.current_file_path: return self.save_file_as()
        else:
            try:
                content = self.text_area.get('1.0', tk.END + "-1c")
                self.sim_os.write_file_for_gui(self.current_file_path, content)
                self.text_modified = False; self.text_area.edit_modified(False); self.update_title()
                print(f"[Editor] Файл сохранен: {self.current_file_path}"); return True
            except Exception as e: messagebox.showerror(tr("error"), f"Ошибка сохранения файла:\n{e}", parent=self); return False

    def save_file_as(self):
        """Сохраняет файл с новым именем (запрашивает путь)."""
        filepath = simpledialog.askstring(tr("editor_save_title"),
                                          "Введите полный путь для сохранения файла в SimOS:",
                                          initialvalue=self.current_file_path if self.current_file_path else "/home/" + self.sim_os.current_user + "/untitled.txt",
                                          parent=self)
        if filepath:
            try:
                # Проверяем, существует ли родительский каталог
                parent_dir = os.path.dirname(filepath).replace("\\","/")
                if not parent_dir: parent_dir = "/" # Если сохраняем в корень
                resolved_parent = self.sim_os._resolve_path(parent_dir)
                parent_node = self.sim_os._get_node_from_path(resolved_parent) if resolved_parent else None
                if parent_node is None or 'children' not in parent_node:
                     raise FileNotFoundError(f"Родительский каталог не существует: {parent_dir}")

                # Проверяем права на запись в родительский каталог
                if not self.sim_os._check_permission(parent_node.get('meta'), 'w'):
                     raise PermissionError(f"Отказано в доступе (запись): {parent_dir}")

                # Проверяем, не пытаемся ли сохранить как существующую папку
                existing_node = parent_node.get('children', {}).get(os.path.basename(filepath))
                if existing_node and 'children' in existing_node:
                     raise IsADirectoryError(f"Нельзя перезаписать каталог: {filepath}")

                # Сохраняем
                self.current_file_path = filepath # Устанавливаем новый путь
                return self.save_file() # Вызываем обычное сохранение
            except Exception as e:
                 messagebox.showerror(tr("error"), f"Ошибка 'Сохранить как':\n{e}", parent=self)
                 return False
        return False # Пользователь нажал Отмена

    def check_save_before_close(self):
        if self.text_modified:
            filename = os.path.basename(self.current_file_path) if self.current_file_path else tr("editor_untitled")
            answer = messagebox.askyesnocancel(tr("editor_save_confirm_title"), tr("editor_save_confirm_msg", filename=filename), parent=self)
            if answer is True: return self.save_file()
            elif answer is False: return True
            else: return False
        return True

    def close_window(self):
        if self.check_save_before_close(): self.destroy()

    def update_language(self):
        self.update_title()
        menubar = tk.Menu(self); self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0); menubar.add_cascade(label=tr("editor_menu_file"), menu=file_menu)
        file_menu.add_command(label=tr("editor_menu_new"), command=self.new_file); file_menu.add_command(label=tr("editor_menu_open"), command=self.open_file)
        file_menu.add_command(label=tr("editor_menu_save"), command=self.save_file); file_menu.add_command(label=tr("editor_menu_save_as"), command=self.save_file_as)
        file_menu.add_separator(); file_menu.add_command(label=tr("editor_menu_exit"), command=self.close_window)
        print("[TextEditor] update_language called")



class SnakeGameWindow(tk.Toplevel):
    """Окно игры Змейка."""
    GAME_WIDTH = 400
    GAME_HEIGHT = 400
    CELL_SIZE = 20
    INITIAL_SPEED = 200 # мс между шагами (меньше = быстрее)
    SPEED_INCREMENT = 0.95 # Множитель для уменьшения задержки (ускорения)
    SNAKE_COLOR = "green"
    FOOD_COLOR = "red"
    BG_COLOR = "black"
    TEXT_COLOR = "white"

    def __init__(self, root, sim_os_instance):
        super().__init__(root)
        self.root_parent = root # Сохраняем ссылку на родителя Toplevel
        self.sim_os = sim_os_instance # SimOS не используется в логике игры, но нужен для консистентности

        self.title(tr("snake_title"))
        # Рассчитываем размер окна с учетом поля для счета
        window_width = self.GAME_WIDTH
        window_height = self.GAME_HEIGHT + 40 # Доп. место для счета
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.transient(root.master)

        self.score = 0
        self.direction = 'Right' # Начальное направление
        self.next_direction = 'Right' # Направление для следующего шага
        self.snake_coords = [(100, 100), (80, 100), (60, 100)] # Начальная змейка (голова первая)
        self.food_coords = None
        self.game_over = False
        self.current_speed = self.INITIAL_SPEED
        self._after_id = None

        # --- Виджеты ---
        self.score_label = tk.Label(self, text=tr("snake_score", score=self.score), font=('Arial', 12), fg=self.TEXT_COLOR, bg=self.BG_COLOR)
        self.score_label.pack(pady=5)

        self.canvas = tk.Canvas(self, bg=self.BG_COLOR, width=self.GAME_WIDTH, height=self.GAME_HEIGHT, highlightthickness=0)
        self.canvas.pack()

        # --- Привязка клавиш ---
        self.bind("<Left>", lambda event: self.change_direction('Left'))
        self.bind("<Right>", lambda event: self.change_direction('Right'))
        self.bind("<Up>", lambda event: self.change_direction('Up'))
        self.bind("<Down>", lambda event: self.change_direction('Down'))

        # --- Запуск игры ---
        self.focus_set() # Устанавливаем фокус на окно игры
        self.create_food()
        self.game_loop()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Останавливает игру при закрытии окна."""
        self.game_over = True # Останавливаем цикл
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        self.destroy()

    def create_food(self):
        """Создает еду в случайном месте, не на змейке."""
        while True:
            x = random.randrange(0, self.GAME_WIDTH // self.CELL_SIZE) * self.CELL_SIZE
            y = random.randrange(0, self.GAME_HEIGHT // self.CELL_SIZE) * self.CELL_SIZE
            self.food_coords = (x, y)
            # Проверяем, не попала ли еда на змейку
            if self.food_coords not in self.snake_coords:
                break
        # Рисуем еду (используем тег 'food' для легкого удаления)
        self.canvas.delete("food")
        self.canvas.create_rectangle(x, y, x + self.CELL_SIZE, y + self.CELL_SIZE, fill=self.FOOD_COLOR, tags="food")

    def draw_snake(self):
        """Рисует змейку на холсте."""
        self.canvas.delete("snake") # Удаляем старую змейку
        for x, y in self.snake_coords:
            self.canvas.create_rectangle(x, y, x + self.CELL_SIZE, y + self.CELL_SIZE, fill=self.SNAKE_COLOR, tags="snake")

    def move_snake(self):
        """Двигает змейку, проверяет столкновения и еду."""
        if self.game_over: return

        # Обновляем направление перед расчетом головы
        self.direction = self.next_direction

        head_x, head_y = self.snake_coords[0]

        # Рассчитываем новую позицию головы
        if self.direction == 'Left': head_x -= self.CELL_SIZE
        elif self.direction == 'Right': head_x += self.CELL_SIZE
        elif self.direction == 'Up': head_y -= self.CELL_SIZE
        elif self.direction == 'Down': head_y += self.CELL_SIZE

        new_head = (head_x, head_y)

        # --- Проверка столкновений ---
        # Со стенами
        if (head_x < 0 or head_x >= self.GAME_WIDTH or
            head_y < 0 or head_y >= self.GAME_HEIGHT):
            self.game_over = True
        # С собой (проверяем со всеми сегментами, кроме головы)
        elif new_head in self.snake_coords:
            self.game_over = True

        if self.game_over:
            self.game_over_display()
            return

        # Добавляем новую голову
        self.snake_coords.insert(0, new_head)

        # --- Проверка на поедание еды ---
        if new_head == self.food_coords:
            self.score += 1
            self.score_label.config(text=tr("snake_score", score=self.score))
            self.create_food()
            # Ускоряем игру
            self.current_speed = int(self.current_speed * self.SPEED_INCREMENT)
            if self.current_speed < 50: self.current_speed = 50 # Минимальная задержка
        else:
            # Удаляем хвост, если еда не съедена
            self.snake_coords.pop()

        self.draw_snake()

    def change_direction(self, new_dir):
        """Изменяет направление движения змейки."""
        # Запрещаем разворот на 180 градусов
        if new_dir == 'Left' and self.direction != 'Right': self.next_direction = new_dir
        elif new_dir == 'Right' and self.direction != 'Left': self.next_direction = new_dir
        elif new_dir == 'Up' and self.direction != 'Down': self.next_direction = new_dir
        elif new_dir == 'Down' and self.direction != 'Up': self.next_direction = new_dir

    def game_loop(self):
        """Основной цикл игры."""
        if self.game_over: return

        self.move_snake()

        # Планируем следующий шаг
        if not self.game_over and self.winfo_exists(): # Проверяем, что окно еще существует
             self._after_id = self.after(int(self.current_speed), self.game_loop)

    def game_over_display(self):
        """Отображает сообщение 'Game Over'."""
        self.canvas.create_text(
            self.GAME_WIDTH / 2, self.GAME_HEIGHT / 2,
            text=tr("snake_game_over"), fill="red", font=('Arial', 24, 'bold'),
            tags="gameover"
        )
        self.canvas.create_text(
            self.GAME_WIDTH / 2, self.GAME_HEIGHT / 2 + 40,
            text=tr("snake_score", score=self.score), fill=self.TEXT_COLOR, font=('Arial', 16),
            tags="gameover"
        )

    def update_language(self):
        """Обновляет язык в игре (заголовок, счет, сообщение Game Over)."""
        self.title(tr("snake_title"))
        self.score_label.config(text=tr("snake_score", score=self.score))
        # Обновляем текст Game Over, если он отображен
        gameover_text_id = self.canvas.find_withtag("gameover")
        if gameover_text_id:
             # Находим конкретные элементы текста (предполагаем их порядок)
             try:
                  self.canvas.itemconfig(gameover_text_id[0], text=tr("snake_game_over"))
                  self.canvas.itemconfig(gameover_text_id[1], text=tr("snake_score", score=self.score))
             except IndexError: pass # Если элементы не найдены
             except tk.TclError: pass # Если холст уже уничтожен
        print("[SnakeGame] update_language called")


# ==============================================================================
# == ГЛАВНЫЙ ЗАПУСК ПРИЛОЖЕНИЯ ==
# ==============================================================================
if __name__ == "__main__":
    CONFIG_FILE = "sim_os_config.json"
    sim_os_data_dir = None

    # --- Загрузка конфигурации или запрос директории ---
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                sim_os_data_dir = config.get("data_directory")
                if sim_os_data_dir and os.path.isdir(sim_os_data_dir):
                    print(f"[Config] Используется директория данных: {sim_os_data_dir}")
                else:
                    print(f"[Config] Путь в конфигурации не найден или некорректен: {sim_os_data_dir}")
                    sim_os_data_dir = None # Сброс, чтобы запросить снова
        except Exception as e:
            print(f"[Config] Ошибка чтения файла конфигурации {CONFIG_FILE}: {e}")
            sim_os_data_dir = None

    if not sim_os_data_dir:
        # Запрашиваем директорию у пользователя
        print("[Config] Запрос директории для данных SimOS...")
        root_ask = tk.Tk()
        root_ask.withdraw() # Скрываем временное окно
        messagebox.showinfo("Настройка SimOS", "Пожалуйста, выберите папку, где SimOS будет хранить свои данные (файл состояния и т.д.).", parent=None)
        chosen_dir = filedialog.askdirectory(title="Выберите папку для данных SimOS", parent=None)
        root_ask.destroy() # Уничтожаем временное окно

        if chosen_dir:
            sim_os_data_dir = chosen_dir
            # Сохраняем выбранный путь в конфиг
            try:
                with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump({"data_directory": sim_os_data_dir}, f, indent=4)
                print(f"[Config] Директория данных сохранена в {CONFIG_FILE}: {sim_os_data_dir}")
            except Exception as e:
                print(f"[Config] Ошибка сохранения файла конфигурации {CONFIG_FILE}: {e}")
                messagebox.showerror("Ошибка конфигурации", f"Не удалось сохранить путь к директории:\n{e}")
                # Продолжаем без сохранения конфига, но используем выбранную папку
        else:
            messagebox.showerror("Настройка SimOS", "Директория не выбрана. SimOS не может продолжить работу.")
            exit()

    # --- Определяем путь к файлу состояния ---
    state_file_full_path = os.path.join(sim_os_data_dir, "sim_os_state.pkl")

    # 1. Создаем/Загружаем экземпляр нашей ОС, передавая путь к файлу состояния
    try:
        sim_os = SimulatedOS(state_file_full_path) # Передаем путь
    except Exception as e:
         print(f"!!! КРИТИЧЕСКАЯ ОШИБКА при инициализации SimulatedOS: {e}")
         traceback.print_exc()
         try:
              root_err = tk.Tk(); root_err.withdraw()
              messagebox.showerror("Ошибка Запуска SimOS", f"Не удалось инициализировать или загрузить состояние ОС:\n\n{e}\n\nСм. консоль для деталей.")
              root_err.destroy()
         except: pass
         exit()

    # 2. Создаем главное окно Tkinter, но пока скрываем его
    root = tk.Tk()
    # --- Добавляем ссылку на DesktopWindow в главное окно ---
    root.desktop_instance = None # Будет установлено в show_desktop
    # --- Конец добавления ---
    root.withdraw()

    # 3. Функция, которая будет вызвана после успешного логина
    def show_desktop():
        try:
            desktop = DesktopWindow(root, sim_os)
            root.desktop_instance = desktop # Сохраняем ссылку
            root.wm_attributes("-topmost", True)
            root.deiconify()
            root.focus_force()
        except Exception as e:
             print(f"!!! ОШИБКА при создании рабочего стола: {e}")
             traceback.print_exc()
             messagebox.showerror("Ошибка GUI", f"Не удалось создать рабочий стол:\n{e}", parent=root)
             root.destroy()

    # 4. Создаем и показываем окно логина
    try:
        login_window = LoginWindow(root, sim_os, show_desktop)
    except Exception as e:
        print(f"!!! ОШИБКА при создании окна входа: {e}")
        traceback.print_exc()
        messagebox.showerror("Ошибка GUI", f"Не удалось создать окно входа:\n{e}")
        root.destroy()
        exit()

    # 5. Запускаем главный цикл Tkinter
    try:
        root.mainloop()
    except Exception as e:
        print(f"\n!!! Непредвиденная ошибка в главном цикле Tkinter (mainloop): {e}")
        traceback.print_exc()
        try:
             if messagebox.askokcancel("Критическая ошибка", "Произошла ошибка.\nСохранить текущее состояние перед выходом?", icon='error'):
                  sim_os.save_state()
        except: pass