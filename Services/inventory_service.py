"""
Inventory Service - Business logic for inventory operations.
"""

import logging
from typing import List, Optional, cast
from sqlalchemy.exc import NoResultFound, IntegrityError

from Models.inventory import Inventory
from Schemas.inventory_schema import InventorySchema
from Api.database import db

logger = logging.getLogger(__name__)


class InventoryService:
    """Service class for Inventory-related business logic."""

    @staticmethod
    def get_inventory_by_id(inventory_id: int) -> Inventory:
        """
        Retrieve an inventory by its ID.

        Args:
            inventory_id: The ID of the inventory to retrieve

        Returns:
            Inventory object if found

        Raises:
            NoResultFound: If inventory doesn't exist
        """
        inventory = db.session.get(Inventory, inventory_id)
        if not inventory:
            logger.warning(f"Inventory with id {inventory_id} not found")
            raise NoResultFound(f"Inventory {inventory_id} not found in database")
        return inventory

    @staticmethod
    def get_inventories_by_user(user_id: int) -> List[Inventory]:
        """
        Retrieve all inventories for a user.

        Args:
            user_id: The ID of the user

        Returns:
            List of Inventory objects

        Raises:
            NoResultFound: If no inventories exist
        """
        inventories = db.session.query(Inventory).filter_by(user_id=user_id).all()
        logger.info(f"Found {len(inventories)} inventories for user {user_id}")
        return inventories

    @staticmethod
    def create_inventory(inventory_data: dict) -> Inventory:
        """
        Create a new inventory.

        Args:
            inventory_data: Dictionary containing inventory information

        Returns:
            Created Inventory object

        Raises:
            ValidationError: If data is invalid
            IntegrityError: If database constraints are violated
        """
        logger.info("Creating new inventory")
        inventory = cast(Inventory, InventorySchema().load(inventory_data))
        db.session.add(inventory)
        db.session.commit()

        db.session.refresh(inventory)
        logger.info(f"Inventory {inventory.id} created successfully")
        return inventory

    @staticmethod
    def update_inventory(inventory_id: int, inventory_data: dict) -> Inventory:
        """
        Update an existing inventory.

        Args:
            inventory_id: The ID of the inventory to update
            inventory_data: Dictionary containing inventory information

        Returns:
            Updated Inventory object

        Raises:
            ValidationError: If data is invalid
            NoResultFound: If inventory doesn't exist
            IntegrityError: If database constraints are violated
        """
        # Verify inventory exists
        existing_inventory = InventoryService.get_inventory_by_id(inventory_id)
        if not existing_inventory:
            raise NoResultFound(f"Inventory with id {inventory_id} not found")
        logger.info(f"Updating inventory {inventory_id}")

        # Handle items separately if present
        if "items" in inventory_data:
            if items := inventory_data.get("items", []):
                existing_inventory.items = items

        updated_inventory = InventorySchema().load(inventory_data)
            
        try:
            merged_inventory = cast(Inventory, db.session.merge(updated_inventory))
            db.session.commit()
            db.session.refresh(merged_inventory)

            logger.info(f"Inventory {inventory_id} updated successfully")
            return merged_inventory

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error updating inventory {inventory_id}: {e}")
            raise

    @staticmethod
    def delete_inventory(inventory_id: int) -> None:
        """
        Delete an inventory by its ID.

        Args:
            inventory_id: The ID of the inventory to delete

        Raises:
            NoResultFound: If inventory doesn't exist
            IntegrityError: If inventory has references that prevent deletion
        """
        inventory = InventoryService.get_inventory_by_id(inventory_id)

        try:
            logger.info(f"Deleting inventory {inventory_id}")
            db.session.delete(inventory)
            db.session.commit()
            logger.info(f"Inventory {inventory_id} deleted successfully")

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Integrity error deleting inventory {inventory_id}: {e}")
            raise IntegrityError(
                f"Cannot delete inventory {inventory_id} due to existing references",
                params=None,
                orig=e,
            )
