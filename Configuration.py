from typing import Optional, Dict, Any

PLAYER_ROLE : Optional[str] = None
SAVE_DIRECTORY : Optional[str] = None

def getConfiguration() -> Dict[str, Any]:
	return {
		"PLAYER_ROLE" : PLAYER_ROLE,
		"SAVE_DIRECTORY" : SAVE_DIRECTORY,
	}