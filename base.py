from functools import wraps
from time import sleep
from typing import TYPE_CHECKING, List, Optional, Tuple

import pyautogui
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


if TYPE_CHECKING:
   from selenium.webdriver.remote.webelement import WebElement
   from selenium.webdriver.firefox.webdriver import WebDriver


def cached_property(fget=None, name_prefix="_x_instance", name=None, loaded=None):
   def decorator(fget):
      @wraps(fget)
      def _wrap_fget(self):
         tmp_name = name or ("%s_%s" % (name_prefix, fget.__name__))
         if getattr(self, tmp_name, None) is None:
            if loaded:
               setattr(self, loaded, True)
            setattr(self, tmp_name, fget(self))
         return getattr(self, tmp_name)

      return property(fget=_wrap_fget)

   if fget:
      return decorator(fget)
   else:
      return decorator





class Base:
   def __del__(self):
      self.driver.close()
      
   @cached_property
   def driver(self) -> "WebDriver":
      driver = Firefox(service=Service(executable_path=GeckoDriverManager().install()))
      driver.implicitly_wait(3) # TODO nowork?
      return driver

   def press_tab(self, elem: "WebElement") -> "WebElement":
      elem.send_keys(Keys.TAB)
      return self.driver.switch_to.active_element

   def press(self, keys: List[str]) -> None:
      pyautogui.press(keys)
      sleep(0.5)

   def write(self, text: str) -> None:
      pyautogui.write(text)
      sleep(0.5)

   def click(self, btn: "WebElement") -> None:
      for moves in ("", 3*['up'], 3*['down']):
         self.driver.execute_script('arguments[0].scrollIntoView();', btn)
         sleep(1)
         self.press(moves)
         try:
            btn.click()
         except:
            pass
         else:
            return
      btn.click()

   def open_tab(self, url: str = "") -> str:
      """ Open url in new tab and return previous window handle. """
      handle = self.driver.current_window_handle
      self.driver.execute_script(f'window.open("{url}");')
      self.driver.switch_to.window(self.driver.window_handles[-1])
      sleep(4)
      return handle

   def close_tab(self, handle: Optional[str] = None) -> None:
      """ 
      Close tab. If tab handle is supplied, move to that tab afterwards,
      else, move to the first open tab.
      """
      self.driver.close()
      handle = handle or self.driver.window_handles[0]
      self.driver.switch_to.window(window_name=handle)
