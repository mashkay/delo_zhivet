import logging

from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, filters

from bot.const import (  # MAKE_DONATION_CMD,
    BECOME_VOLUNTEER_CMD,
    END_CMD,
    REPORT_ECO_PROBLEM_CMD,
    SPECIFY_ACTIVITY_RADIUS_CMD,
    SPECIFY_CAR_AVAILABILITY_CMD,
    SPECIFY_CITY_CMD,
)
from core.settings import settings

from .handlers.common import end_describing, help_command, stop, stop_nested
from .handlers.participation import make_donation
from .handlers.pollution import (
    input,
    save_and_exit_pollution,
    save_comment,
    save_foto,
    save_location,
    select_option_to_report_about_pollution,
)
from .handlers.social import (
    input_social_data,
    report_about_social_problem,
    save_and_exit_from_social_problem,
    save_social_problem_data,
)
from .handlers.start import start
from .handlers.state_constants import (
    ADDING_SOCIAL_TASK,
    ADDING_VOLUNTEER,
    CAR_COMMAND,
    CITY_COMMAND,
    POLLUTION_COMMENT,
    POLLUTION_COORDINATES,
    POLLUTION_FOTO,
    RADIUS_COMMAND,
    SAVE,
    SELECTING_ACTION,
    SELECTING_FEATURE,
    SELECTING_OVER,
    SOCIAL_ADDRESS,
    SOCIAL_COMMENT,
    SOCIAL_PROBLEM_TYPING,
    TYPING,
    TYPING_CITY,
)
from .handlers.volunteer import (
    add_volunteer,
    ask_for_input_city,
    handle_car_input,
    handle_city_input,
    handle_radius_input,
    save_and_exit_volunteer,
    save_input,
)

# from telegram.ext.filters import Regex


def start_bot() -> None:
    """Запуск бота"""
    aps_logger = logging.getLogger("apscheduler")
    aps_logger.setLevel(logging.DEBUG)
    bot = Application.builder().token(settings.telegram_bot_token).build()

    add_volunteer_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_volunteer, pattern=BECOME_VOLUNTEER_CMD)],
        states={
            ADDING_VOLUNTEER: [
                CallbackQueryHandler(ask_for_input_city, pattern=SPECIFY_CITY_CMD),
                CallbackQueryHandler(handle_radius_input, pattern=SPECIFY_ACTIVITY_RADIUS_CMD),
                CallbackQueryHandler(handle_car_input, pattern=SPECIFY_CAR_AVAILABILITY_CMD),
                CallbackQueryHandler(save_and_exit_volunteer, pattern="^" + SAVE + "$"),
            ],
            TYPING_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city_input)],
            SELECTING_OVER: [
                CallbackQueryHandler(save_input, pattern="^" + CITY_COMMAND),
                CallbackQueryHandler(save_input, pattern="^" + RADIUS_COMMAND),
                CallbackQueryHandler(save_input, pattern="^" + CAR_COMMAND),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(end_describing, pattern=END_CMD),
            CommandHandler("stop", stop_nested),
        ],
    )

    add_pollution_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_option_to_report_about_pollution, pattern=REPORT_ECO_PROBLEM_CMD)],
        states={
            SELECTING_FEATURE: [
                CallbackQueryHandler(input, pattern="^" + POLLUTION_COMMENT + "$"),
                CallbackQueryHandler(input, pattern="^" + POLLUTION_COORDINATES + "$"),
                CallbackQueryHandler(input, pattern="^" + POLLUTION_FOTO + "$"),
                CallbackQueryHandler(save_and_exit_pollution, pattern="^" + SAVE + "$"),
            ],
            TYPING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_comment),
                MessageHandler(filters.PHOTO & ~filters.COMMAND, save_foto),
                MessageHandler(filters.LOCATION & ~filters.COMMAND, save_location),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(end_describing, pattern=END_CMD),
            CommandHandler("stop", stop_nested),
        ],
    )

    add_social_conv = ConversationHandler(
        # OK
        entry_points=[
            CallbackQueryHandler(
                report_about_social_problem,
                pattern=ADDING_SOCIAL_TASK,
            )
        ],
        states={
            SELECTING_FEATURE: [
                CallbackQueryHandler(input_social_data, pattern="^" + SOCIAL_ADDRESS + "$"),
                CallbackQueryHandler(input_social_data, pattern="^" + SOCIAL_COMMENT + "$"),
                CallbackQueryHandler(save_and_exit_from_social_problem, pattern="^" + SAVE + "$"),
            ],
            SOCIAL_PROBLEM_TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_social_problem_data)],
        },
        # OK
        fallbacks=[
            CallbackQueryHandler(end_describing, pattern=END_CMD),
            CommandHandler("stop", stop_nested),
        ],
    )
    # add_donation_conv = ConversationHandler(
    #     entry_points=[
    #         CallbackQueryHandler(add_volunteer, pattern=BECOME_VOLUNTEER_CMD)
    #     ],
    #     fallbacks=[
    #         CallbackQueryHandler(end_describing, pattern=END_CMD),
    #         CommandHandler("stop", stop_nested),
    #     ],
    # )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: [
                add_volunteer_conv,
                add_pollution_conv,
                add_social_conv,
            ],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    bot.add_handler(conv_handler)

    # bot.add_handler(MessageHandler(Regex(MAKE_DONATION_CMD), make_donation)) # noqa
    bot.add_handler(CommandHandler("try", make_donation))
    bot.add_handler(CommandHandler("help", help_command))

    aps_logger.info("Service started.")

    bot.run_polling()

    aps_logger.info("Service stopped.")
