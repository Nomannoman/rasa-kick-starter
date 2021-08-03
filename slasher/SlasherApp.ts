import {
    IAppAccessors,
    ILogger,
    IConfigurationExtend,
} from '@rocket.chat/apps-engine/definition/accessors';
import { App } from '@rocket.chat/apps-engine/definition/App';
import { IAppInfo } from '@rocket.chat/apps-engine/definition/metadata';
import { MailCommand } from './commands/mail';
import { HandoffCommand } from './commands/handoff';
import { LoginCommand } from './commands/login';



export class SlasherApp extends App {
    constructor(info: IAppInfo, logger: ILogger, accessors: IAppAccessors) {
        super(info, logger, accessors);
    }

    protected async extendConfiguration(configuration: IConfigurationExtend): Promise<void> {
        await configuration.slashCommands.provideSlashCommand(new MailCommand(this));
        await configuration.slashCommands.provideSlashCommand(new HandoffCommand(this));
        await configuration.slashCommands.provideSlashCommand(new LoginCommand(this));

    }
}
