"""The tests for Lawn Mower device actions."""

import pytest
from pytest_unordered import unordered

from homeassistant.components.device_automation import DeviceAutomationType
from homeassistant.components.lawn_mower import DOMAIN
from homeassistant.components.lawn_mower.const import LawnMowerEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from tests.common import MockConfigEntry, async_get_device_automations


@pytest.mark.parametrize(
    ("set_state", "features_reg", "features_state"),
    [
        (
            True,
            LawnMowerEntityFeature.DOCK,
            "dock",
        ),
    ],
)
async def test_get_actions(
    hass: HomeAssistant,
    device_registry: dr.DeviceRegistry,
    entity_registry: er.EntityRegistry,
    set_state: bool,
    features_reg: LawnMowerEntityFeature,
    features_state: LawnMowerEntityFeature,
) -> None:
    """Test we get the expected actions from a lawn_mower."""
    config_entry = MockConfigEntry(domain="test", data={})
    config_entry.add_to_hass(hass)
    device_entry = device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, "12:34:56:AB:CD:EF")},
    )
    entity_registry.async_get_or_create(
        DOMAIN,
        "test",
        "5678",
        device_id=device_entry.id,
        supported_features=features_reg,
    )
    if set_state:
        hass.states.async_set(
            f"{DOMAIN}.test_5678", "attributes", {"supported_features": features_state}
        )
    expected_actions = [
        {
            "domain": DOMAIN,
            "type": "dock",
            "device_id": device_entry.id,
            "entity_id": f"{DOMAIN}.test_5678",
            "metadata": {"secondary": False},
        }
        for action in ["dock"]
    ]
    actions = await async_get_device_automations(
        hass, DeviceAutomationType.ACTION, device_entry.id
    )
    assert actions == unordered(expected_actions)

    # @pytest.mark.parametrize(
    #     ("hidden_by", "entity_category"),
    #     [
    #         (er.RegistryEntryHider.INTEGRATION, None),
    #         (er.RegistryEntryHider.USER, None),
    #         (None, EntityCategory.CONFIG),
    #         (None, EntityCategory.DIAGNOSTIC),
    #     ],
    # )
    # async def test_get_actions_hidden_auxiliary(
    #     hass: HomeAssistant,
    #     device_registry: dr.DeviceRegistry,
    #     entity_registry: er.EntityRegistry,
    #     hidden_by: er.RegistryEntryHider | None,
    #     entity_category: EntityCategory | None,
    # ):
    #     """Test we get the expected actions from a hidden or auxiliary entity."""
    #     config_entry = MockConfigEntry(domain="test", data={})
    #     config_entry.add_to_hass(hass)
    #     device_entry = device_registry.async_get_or_create(
    #         config_entry_id=config_entry.entry_id,
    #         connections={(dr.CONNECTION_NETWORK_MAC, "12:34:56:AB:CD:EF")},
    #     )
    #     entity_registry.async_get_or_create(
    #         DOMAIN,
    #         "test",
    #         "5678",
    #         device_id=device_entry.id,
    #         entity_category=entity_category,
    #         hidden_by=hidden_by,
    #     )
    #     expected_actions = [
    #         {
    #             "domain": DOMAIN,
    #             "type": action,
    #             "device_id": device_entry.id,
    #             "entity_id": f"{DOMAIN}.test_5678",
    #             "metadata": {"secondary": True},
    #         }
    #         for action in ["mow", "dock", "pause"]
    #     ]
    #     actions = await async_get_device_automations(
    #         hass, DeviceAutomationType.ACTION, device_entry.id
    #     )
    #     assert actions == unordered(expected_actions)

    # async def test_action(hass: HomeAssistant) -> None:
    #     """Test for turn_on and turn_off actions."""
    #     assert await async_setup_component(
    #         hass,
    #         automation.DOMAIN,
    #         {
    #             automation.DOMAIN: [
    #                 {
    #                     "trigger": {
    #                         "platform": "event",
    #                         "event_type": "test_event_mow",
    #                     },
    #                     "action": {
    #                         "domain": DOMAIN,
    #                         "device_id": "abcdefgh",
    #                         "entity_id": "lawn_mower.entity",
    #                         "type": "mow",
    #                     },
    #                 },
    #                 {
    #                     "trigger": {
    #                         "platform": "event",
    #                         "event_type": "test_event_dock",
    #                     },
    #                     "action": {
    #                         "domain": DOMAIN,
    #                         "device_id": "abcdefgh",
    #                         "entity_id": "lawn_mower.entity",
    #                         "type": "dock",
    #                     },
    #                 },
    #             ]
    #         },
    #     )

    #     turn_off_calls = async_mock_service(hass, "lawn_mower", "mow")
    #     turn_on_calls = async_mock_service(hass, "lawn_mower", "dock")

    #     hass.bus.async_fire("test_event_mow")
    #     await hass.async_block_till_done()
    #     assert len(turn_off_calls) == 1
    #     assert len(turn_on_calls) == 0

    #     hass.bus.async_fire("test_event_dock")
    #     await hass.async_block_till_done()
    #     assert len(turn_off_calls) == 1
    assert len(turn_on_calls) == 1
