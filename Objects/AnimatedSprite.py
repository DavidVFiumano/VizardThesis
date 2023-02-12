from typing import Iterable, Union
from collections import abc
from dataclasses import dataclass

import viz
import vizact

class AnimatedSprite:
	
	def __init__(self, modelFilePath : str, *, 
						position : Union[Iterable[float], None] = None, 
						scale : float = 1, 
						spinAxis : Iterable[float] = tuple([0, 1, 0]), 
						spinDegPerSecond : Union[float, None] = None, 
						name : Union[str, None] = None):
							
		self.model = viz.addChild(modelFilePath)
		if position is not None:
			self.model.setPosition(*position)
		
		if scale is not None:
			if not isinstance(scale, abc.Iterable):
				self.model.setScale(scale, scale, scale)
			else:
				self.model.setScale(*scale)
				
		self.model.addAction(vizact.spin(spinAxis[0], spinAxis[1], spinAxis[2], spinDegPerSecond))
		
		self.name = name
		
	def getModel(self):
		return self.model
		
	def remove(self, children : bool = True):
		self.model.remove(children)
		
	def getName(self) -> str:
		return self.name