# -*- coding: utf-8 -*-
"""Clase que representa un producto textil"""

class Producto:
    def __init__(self, id, nombre, tipo_tela, talla, cantidad, color="N/A"):
        self.id = id
        self.nombre = nombre
        self.tipo_tela = tipo_tela
        self.talla = talla
        self.cantidad = cantidad
        self.color = color

    def __str__(self):
        return f"{self.id:3} | {self.nombre:20} | {self.tipo_tela:12} | {self.talla:5} | {self.color:10} | {self.cantidad:5}"

    def to_dict(self):
        """Convierte el producto a diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo_tela": self.tipo_tela,
            "talla": self.talla,
            "cantidad": self.cantidad,
            "color": self.color
        }
    
    @staticmethod
    def from_dict(data):
        """Crea un producto desde un diccionario"""
        return Producto(
            data['id'],
            data['nombre'],
            data['tipo_tela'],
            data['talla'],
            data['cantidad'],
            data.get('color', 'N/A')
        )