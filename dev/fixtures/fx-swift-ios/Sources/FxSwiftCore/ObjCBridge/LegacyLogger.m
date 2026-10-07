// LegacyLogger.m
// Implementacion del logger heredado Objective-C. Compilado por el
// target `FxSwiftApp` (no por SwiftPM, ver Package.swift `exclude`).
// Se expone a Swift via el bridging header `FxSwift-Bridging-Header.h`.

#import "LegacyLogger.h"

NSNotificationName const LegacyLoggerDidLogNotification =
    @"LegacyLoggerDidLogNotification";

@interface LegacyLogger ()
@property (nonatomic, readwrite) NSUInteger callCount;
@end

@implementation LegacyLogger

// Trampa E4: `@dynamic` indica que los setters/getters los provee el
// runtime (KVO necesita este atributo para que observeProperty:
// funcione correctamente). Si fuera `@synthesize`, KVO fallaria
// silenciosamente.
@dynamic lastMessage;

+ (instancetype)sharedLogger {
    static LegacyLogger *instance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        instance = [[self alloc] init];
    });
    return instance;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        _callCount = 0;
    }
    return self;
}

- (void)log:(NSString *)message {
    self.callCount += 1;
    self.lastMessage = message;
    NSDictionary *userInfo = @{ @"message": message ?: @"" };
    [[NSNotificationCenter defaultCenter]
        postNotificationName:LegacyLoggerDidLogNotification
                      object:self
                    userInfo:userInfo];
}

- (void)clear {
    self.lastMessage = nil;
    self.callCount = 0;
}

- (void)registerForNotifications {
    // Trampa E4: este metodo existe pero el caller (SettingsHostController)
    // nunca lo invoca. El observer en Swift nunca se registra.
}

@end
