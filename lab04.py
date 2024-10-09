class Item:
    def __init__(self, name, description='', rarity='common'):
        self.name = name
        self.description = description
        self.rarity = rarity
        self._ownership = ''  # Private attribute for ownership

    def pick_up(self, character: str):
        self._ownership = character
        return f"{self.name} is now owned by {self._ownership}"

    def throw_away(self):
        self._ownership = ''
        return f"{self.name} is thrown away"

    def use(self):
        if self._ownership:
            return f"{self.name} is used"
        return ''

    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description}"


class Weapon(Item):
    def __init__(self, name, damage, weapon_type, rarity='common'):
        super().__init__(name, rarity=rarity)
        self.damage = damage
        self.type = weapon_type
        self.active = False
        self.passive_attack_modifier = 1.0 if rarity != 'legendary' else 1.15

    def equip(self):
        self.active = True
        print(f"{self.name} is equipped by {self._ownership}")

    def use(self):
        if self.active and self._ownership:
            damage_done = self.damage * self.passive_attack_modifier
            print(f"{self.name} is used, dealing {damage_done} damage")
        else:
            return ''


class Shield(Item):
    def __init__(self, name, defense, broken=False, rarity='common'):
        super().__init__(name, rarity=rarity)
        self.defense = defense
        self.broken = broken
        self.active = False
        self.passive_defense_modifier = 1.0 if rarity != 'legendary' else 1.10

    def equip(self):
        self.active = True
        print(f"{self.name} is equipped by {self._ownership}")

    def use(self):
        if self.active and self._ownership:
            if self.broken:
                defense_power = self.defense * self.passive_defense_modifier * 0.5
            else:
                defense_power = self.defense * self.passive_defense_modifier
            print(f"{self.name} is used, blocking {defense_power} damage")
        else:
            return ''


class Potion(Item):
    def __init__(self, name, potion_type, value, effective_time=0, rarity='common'):
        super().__init__(name, rarity=rarity)
        self.potion_type = potion_type
        self.value = value
        self.effective_time = effective_time
        self.empty = False

    def use(self):
        if not self.empty and self._ownership:
            print(f"{self.name} is consumed, {self.potion_type} increased by {self.value} for {self.effective_time} seconds")
            self.empty = True
        else:
            print("Potion is empty")

    @classmethod
    def from_ability(cls, name, owner, potion_type):
        return cls(name, potion_type, value=50, effective_time=30, rarity='common')


# Main function with example usage
def main():
    # Creating some items
    long_bow = Weapon(name='Belthronding', damage=5000, weapon_type='bow', rarity='legendary')
    wooden_shield = Shield(name='Wooden Lid', defense=5, broken=True)
    attack_potion = Potion.from_ability(name='Atk Potion Temp', owner='Beleg', potion_type='attack')

    # Testing weapon
    print(long_bow.pick_up('Beleg'))
    long_bow.equip()
    long_bow.use()

    # Testing shield
    print(wooden_shield.pick_up('Beleg'))
    wooden_shield.equip()
    wooden_shield.use()
    print(wooden_shield.throw_away())
    wooden_shield.use()

    # Testing potion
    attack_potion.use()
    attack_potion.use()  # This should output "Potion is empty"

if __name__ == '__main__':
    main()

