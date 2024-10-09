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
        if self.rarity == 'legendary':
            return f"*** Legendary Item ***\n{self.name} ({self.rarity}): {self.description}"
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
            print(f"{self.attack_move()} {self.name} is used, dealing {damage_done} damage")
        else:
            return ''

    def attack_move(self):
        raise NotImplementedError("This method should be overridden by subclasses")


class SingleHandedWeapon(Weapon):
    def attack_move(self):
        return f"{self._ownership} slashes with"


class DoubleHandedWeapon(Weapon):
    def attack_move(self):
        return f"{self._ownership} spins with"


class Pike(Weapon):
    def attack_move(self):
        return f"{self._ownership} thrusts with"


class RangedWeapon(Weapon):
    def attack_move(self):
        return f"{self._ownership} shoots with"


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


class Inventory:
    def __init__(self, owner=None):
        self.owner = owner
        self.items = []

    def add_item(self, item):
        item.pick_up(self.owner)
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            item.throw_away()
            self.items.remove(item)

    def view(self, type=None):
        if type:
            for item in self.items:
                if isinstance(item, eval(type.capitalize())):  # Dynamically evaluate the type of item
                    print(item)
        else:
            for item in self.items:
                print(item)

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, item):
        return item in self.items


# Main function with example usage
def main():
    # Creating weapons
    master_sword = SingleHandedWeapon(name='Master Sword', damage=300, weapon_type='sword', rarity='legendary')
    muramasa = DoubleHandedWeapon(name='Muramasa', damage=580, weapon_type='katana', rarity='legendary')
    gungnir = Pike(name='Gungnir', damage=290, weapon_type='spear', rarity='legendary')
    belthronding = RangedWeapon(name='Belthronding', damage=500, weapon_type='bow', rarity='legendary')

    # Creating other items
    hp_potion = Potion.from_ability(name='HP Potion', owner='Beleg', potion_type='HP')
    broken_pot_lid = Shield(name='Broken Pot Lid', defense=5, broken=True)
    round_shield = Shield(name='Round Shield', defense=30, rarity='epic')

    # Creating inventory
    beleg_backpack = Inventory(owner='Beleg')
    beleg_backpack.add_item(belthronding)
    beleg_backpack.add_item(hp_potion)
    beleg_backpack.add_item(master_sword)
    beleg_backpack.add_item(broken_pot_lid)
    beleg_backpack.add_item(muramasa)
    beleg_backpack.add_item(gungnir)
    beleg_backpack.add_item(round_shield)

    # Viewing items
    beleg_backpack.view(type='shield')  # Viewing only shields
    beleg_backpack.view()  # Viewing all items

    # Removing item
    beleg_backpack.remove_item(broken_pot_lid)

    # Checking if an item is in the inventory
    if master_sword in beleg_backpack:
        master_sword.equip()
        print(master_sword)  # Show off legendary item
        master_sword.use()  # Beleg slashes with the Master Sword

    # Iterating over items
    for item in beleg_backpack:
        if isinstance(item, Weapon):
            beleg_backpack.view(type='weapon')


if __name__ == '__main__':
    main()
