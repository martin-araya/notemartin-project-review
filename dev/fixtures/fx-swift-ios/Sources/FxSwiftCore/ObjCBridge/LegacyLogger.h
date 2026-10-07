// LegacyLogger.h
// Modulo Objective-C expuesto a Swift via bridging header (trampa E4).
// - `@objc dynamic` en una property: KVO dispara observers
//   automaticamente sin intervencion manual.
// - NSNotificationCenter.defaultCenter para notificar a los listeners
//   cuando se loguea un mensaje.
// - KVO sobre `lastMessage` para que SwiftUI/Combine observen cambios.

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

extern NSNotificationName const LegacyLoggerDidLogNotification;

@interface LegacyLogger : NSObject

@property (nonatomic, copy, nullable) NSString *lastMessage;
@property (nonatomic, readonly) NSUInteger callCount;

+ (instancetype)sharedLogger;

- (void)log:(NSString *)message;
- (void)clear;
- (void)registerForNotifications;

@end

NS_ASSUME_NONNULL_END
