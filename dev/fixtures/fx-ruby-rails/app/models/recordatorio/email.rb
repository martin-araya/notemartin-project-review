class Recordatorio
  class Email < Recordatorio
    validates :destinatario_email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }

    def canal
      "email"
    end
  end
end
